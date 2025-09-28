from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database import get_session
from app.models import Post, Research, News, User

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def dashboard_home(
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    # 통계 데이터 수집
    post_count = await session.scalar(select(func.count(Post.id)))
    research_count = await session.scalar(select(func.count(Research.id)))
    news_count = await session.scalar(select(func.count(News.id)))
    user_count = await session.scalar(select(func.count(User.id)))

    # 최근 게시물
    recent_posts = await session.execute(
        select(Post).order_by(Post.created_at.desc()).limit(5)
    )
    recent_posts = recent_posts.scalars().all()

    # 최근 연구
    recent_research = await session.execute(
        select(Research).order_by(Research.created_at.desc()).limit(3)
    )
    recent_research = recent_research.scalars().all()

    # 최신 뉴스
    latest_news = await session.execute(
        select(News).where(News.is_featured == True).order_by(News.published_at.desc()).limit(3)
    )
    latest_news = latest_news.scalars().all()

    stats = {
        "posts": post_count or 0,
        "research": research_count or 0,
        "news": news_count or 0,
        "users": user_count or 0
    }

    return templates.TemplateResponse("dashboard/index.html", {
        "request": request,
        "stats": stats,
        "recent_posts": recent_posts,
        "recent_research": recent_research,
        "latest_news": latest_news
    })

@router.get("/analytics", response_class=HTMLResponse)
async def dashboard_analytics(
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    # 월별 게시물 통계
    monthly_posts = await session.execute(
        select(
            func.strftime('%Y-%m', Post.created_at).label('month'),
            func.count(Post.id).label('count')
        ).group_by(func.strftime('%Y-%m', Post.created_at))
        .order_by(func.strftime('%Y-%m', Post.created_at))
    )
    monthly_data = monthly_posts.all()

    return templates.TemplateResponse("dashboard/analytics.html", {
        "request": request,
        "monthly_data": monthly_data
    })

@router.get("/research", response_class=HTMLResponse)
async def dashboard_research(
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    # 연구팀별 통계
    research_by_type = await session.execute(
        select(
            Research.research_type,
            func.count(Research.id).label('count')
        ).group_by(Research.research_type)
    )
    research_stats = research_by_type.all()

    # 진행 상태별 연구
    research_by_status = await session.execute(
        select(
            Research.status,
            func.count(Research.id).label('count')
        ).group_by(Research.status)
    )
    status_stats = research_by_status.all()

    return templates.TemplateResponse("dashboard/research.html", {
        "request": request,
        "research_stats": research_stats,
        "status_stats": status_stats
    })