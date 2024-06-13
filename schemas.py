# schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class PostBase(BaseModel):
    domain: str

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    date_post: datetime

    class Config:
        orm_mode = True

class ThemeBase(BaseModel):
    name: str
    name_file_to_key: str
    folder_to_pict: str

class ThemeCreate(ThemeBase):
    pass

class Theme(ThemeBase):
    id: int

    class Config:
        orm_mode = True

class SiteBase(BaseModel):
    domain: str
    login: str
    password: str
    theme_id: int

class SiteCreate(SiteBase):
    pass

class Site(SiteBase):
    id: int
    theme: Optional[Theme] = None
    posts: List[Post] = []

    class Config:
        orm_mode = True
