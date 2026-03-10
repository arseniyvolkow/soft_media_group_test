from pydantic import BaseModel, HttpUrl, Field


class LinkCreate(BaseModel):
    original_url: str = Field(..., description="Url который будет сокращен")


class LinkShortenResponse(BaseModel):
    short_id: str
    original_url: str


class LinkStats(BaseModel):
    short_id: str
    original_url: str
    visits_count: int

    class Config:
        from_attributes = True
