from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from models import Link
from utils import Base62Encoder
from pydantic import HttpUrl


class LinksService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.encoder = Base62Encoder()

    async def create_short_link(self, original_url: HttpUrl | str) -> str:
        # Convert Pydantic HttpUrl to string if necessary
        url_str = str(original_url)

        query = select(Link).where(Link.original_url == url_str)
        result = await self.db.execute(query)
        link = result.scalar_one_or_none()

        if not link:
            link = Link(original_url=url_str)
            self.db.add(link)
            try:
                await self.db.commit()
                await self.db.refresh(link)
            except IntegrityError:
                # Handle concurrent creation for the same URL
                await self.db.rollback()
                query = select(Link).where(Link.original_url == url_str)
                result = await self.db.execute(query)
                link = result.scalar_one_or_none()

        return self.encoder.encode(link.id)

    async def get_stats(self, short_id: str) -> Link | None:
        link_id = self.encoder.decode(short_id)
        if link_id is None:
            return None

        query = select(Link).where(Link.id == link_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_original_url_and_increment(self, short_id: str) -> str | None:
        link_id = self.encoder.decode(short_id)
        if link_id is None:
            return None

        query = (
            update(Link)
            .where(Link.id == link_id)
            .values(visits_count=Link.visits_count + 1)
            .returning(Link.original_url)
        )

        result = await self.db.execute(query)
        original_url = result.scalar_one_or_none()
        await self.db.commit()

        return original_url
