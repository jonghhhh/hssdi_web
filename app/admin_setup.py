from fastcrud import FastCRUD
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import User, Post, Category, Research, News
from app.schemas import UserCreate, UserUpdate, PostCreate, PostUpdate, CategoryCreate, ResearchCreate, NewsCreate
from app.config import settings

def setup_admin():
    admin_app = FastAPI()

    # Create CRUD instances for each model
    user_crud = FastCRUD(User)
    post_crud = FastCRUD(Post)
    category_crud = FastCRUD(Category)
    research_crud = FastCRUD(Research)
    news_crud = FastCRUD(News)

    # Add admin routes for users
    @admin_app.get("/users")
    async def get_users(session: AsyncSession = Depends(get_session)):
        return await user_crud.get_multi(db=session)

    @admin_app.post("/users")
    async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
        return await user_crud.create(db=session, object=user)

    @admin_app.put("/users/{user_id}")
    async def update_user(user_id: int, user: UserUpdate, session: AsyncSession = Depends(get_session)):
        return await user_crud.update(db=session, object=user, id=user_id)

    @admin_app.delete("/users/{user_id}")
    async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
        return await user_crud.delete(db=session, id=user_id)

    # Add admin routes for posts
    @admin_app.get("/posts")
    async def get_posts(session: AsyncSession = Depends(get_session)):
        return await post_crud.get_multi(db=session)

    @admin_app.post("/posts")
    async def create_post(post: PostCreate, session: AsyncSession = Depends(get_session)):
        return await post_crud.create(db=session, object=post)

    @admin_app.put("/posts/{post_id}")
    async def update_post(post_id: int, post: PostUpdate, session: AsyncSession = Depends(get_session)):
        return await post_crud.update(db=session, object=post, id=post_id)

    @admin_app.delete("/posts/{post_id}")
    async def delete_post(post_id: int, session: AsyncSession = Depends(get_session)):
        return await post_crud.delete(db=session, id=post_id)

    # Similar routes for other models...
    @admin_app.get("/categories")
    async def get_categories(session: AsyncSession = Depends(get_session)):
        return await category_crud.get_multi(db=session)

    @admin_app.post("/categories")
    async def create_category(category: CategoryCreate, session: AsyncSession = Depends(get_session)):
        return await category_crud.create(db=session, object=category)

    @admin_app.get("/research")
    async def get_research(session: AsyncSession = Depends(get_session)):
        return await research_crud.get_multi(db=session)

    @admin_app.post("/research")
    async def create_research(research: ResearchCreate, session: AsyncSession = Depends(get_session)):
        return await research_crud.create(db=session, object=research)

    @admin_app.get("/news")
    async def get_news(session: AsyncSession = Depends(get_session)):
        return await news_crud.get_multi(db=session)

    @admin_app.post("/news")
    async def create_news(news: NewsCreate, session: AsyncSession = Depends(get_session)):
        return await news_crud.create(db=session, object=news)

    return admin_app