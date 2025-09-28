from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None

class User(UserBase):
    id: int
    is_admin: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PostBase(BaseModel):
    title: str
    content: str
    category_id: Optional[int] = None
    is_published: bool = True

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category_id: Optional[int] = None
    is_published: Optional[bool] = None

class Post(PostBase):
    id: int
    author_id: int
    views: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ResearchBase(BaseModel):
    title: str
    description: Optional[str] = None
    research_type: Optional[str] = None
    status: str = "진행중"
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class ResearchCreate(ResearchBase):
    pass

class Research(ResearchBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class NewsBase(BaseModel):
    title: str
    content: str
    is_featured: bool = False
    published_at: Optional[datetime] = None

class NewsCreate(NewsBase):
    pass

class News(NewsBase):
    id: int
    author_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None