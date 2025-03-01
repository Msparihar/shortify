from pydantic import BaseModel, HttpUrl
from datetime import datetime


class URLBase(BaseModel):
    target_url: HttpUrl


class URLCreate(URLBase):
    pass


class URL(URLBase):
    id: str
    short_code: str
    clicks: int
    created_at: datetime

    class Config:
        from_attributes = True


class URLList(BaseModel):
    urls: list[URL]
