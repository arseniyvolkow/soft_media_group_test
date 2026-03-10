import pytest
from unittest.mock import AsyncMock, MagicMock
from links_service import LinksService
from utils import Base62Encoder

def test_encode():
    encoder = Base62Encoder()
    assert encoder.encode(0) == "0"
    assert encoder.encode(1) == "1"
    assert encoder.encode(10) == "a"
    assert encoder.encode(61) == "Z"
    assert encoder.encode(62) == "10"

def test_decode():
    encoder = Base62Encoder()
    assert encoder.decode("0") == 0
    assert encoder.decode("1") == 1
    assert encoder.decode("a") == 10
    assert encoder.decode("Z") == 61
    assert encoder.decode("10") == 62
    assert encoder.decode("invalid!") is None

@pytest.mark.asyncio
async def test_create_short_link_new():
    mock_db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_db.execute.return_value = mock_result
    
    service = LinksService(db=mock_db)
    
    def side_effect(link):
        link.id = 123
        return None
        
    mock_db.refresh.side_effect = side_effect
    
    short_id = await service.create_short_link("http://example.com")
    
    assert short_id == Base62Encoder.encode(123)
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()

@pytest.mark.asyncio
async def test_get_stats_not_found():
    mock_db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_db.execute.return_value = mock_result
    
    service = LinksService(db=mock_db)
    result = await service.get_stats("abc")
    
    assert result is None
