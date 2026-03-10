from fastapi import FastAPI, status, HTTPException
from dependencies import LinkServiceDependency
from fastapi.responses import RedirectResponse
from schemas import LinkCreate, LinkShortenResponse, LinkStats

app = FastAPI()

@app.post('/shorten', response_model=LinkShortenResponse)
async def shorten_url(link_service: LinkServiceDependency, data: LinkCreate):
    short_id = await link_service.create_short_link(data.original_url)
    return LinkShortenResponse(short_id=short_id, original_url=data.original_url)

@app.get('/{short_id}')
async def redirect_to_original_url(link_service: LinkServiceDependency, short_id: str):
    original_url = await link_service.get_original_url_and_increment(short_id)
    if not original_url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found")
    return RedirectResponse(original_url, status_code=status.HTTP_302_FOUND)

@app.get('/stats/{short_id}', response_model=LinkStats)
async def get_stats(link_service: LinkServiceDependency, short_id: str):
    link = await link_service.get_stats(short_id)
    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found")
    
    return LinkStats(
        short_id=short_id,
        original_url=link.original_url,
        visits_count=link.visits_count
    )