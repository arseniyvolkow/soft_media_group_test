from pydantic import BaseModel, HttpUrl, Field


class LinkCreate(BaseModel):
    original_url: HttpUrl = Field(
        ..., 
        description="Url который будет сокращен",
        examples=["https://www.google.com"]
    )


class LinkShortenResponse(BaseModel):
    short_id: str
    original_url: HttpUrl


class LinkStats(BaseModel):
    short_id: str
    original_url: HttpUrl
    visits_count: int

    class Config:
        from_attributes = True
