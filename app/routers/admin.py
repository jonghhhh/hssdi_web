from fastapi import APIRouter, Depends, HTTPException, status, Form, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
from sqlalchemy.orm import selectinload
from datetime import timedelta
from typing import Optional

from app.database import get_session
from app.auth import authenticate_user, create_access_token, get_current_admin_user
from app.schemas import Token, User
from app.models import Post, Category, User as UserModel
from app.config import settings

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session)
):
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_admin_user)):
    return current_user

# 관리자 로그인 페이지
@router.get("/login", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    return templates.TemplateResponse("admin/login.html", {"request": request})

# 관리자 인증 체크 함수
def check_admin_auth(request: Request):
    if not request.session.get("admin_logged_in"):
        return RedirectResponse(url="/admin/login", status_code=303)
    return True

# 관리자 대시보드
@router.get("/dashboard", response_class=HTMLResponse)
async def admin_dashboard(
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    # 인증 체크
    if not request.session.get("admin_logged_in"):
        return RedirectResponse(url="/admin/login", status_code=303)

    # 통계 데이터 조회
    posts_count = await session.scalar(select(func.count(Post.id)))
    categories_count = await session.scalar(select(func.count(Category.id)))
    users_count = await session.scalar(select(func.count(UserModel.id)))

    # 최근 게시물
    recent_posts_result = await session.execute(
        select(Post).options(
            selectinload(Post.author),
            selectinload(Post.category)
        ).order_by(desc(Post.created_at)).limit(5)
    )
    recent_posts = recent_posts_result.scalars().all()

    return templates.TemplateResponse("admin/admin.html", {
        "request": request,
        "posts_count": posts_count,
        "categories_count": categories_count,
        "users_count": users_count,
        "recent_posts": recent_posts
    })

# 게시물 관리
@router.get("/posts", response_class=HTMLResponse)
async def admin_posts(
    request: Request,
    page: int = 1,
    search: Optional[str] = None,
    session: AsyncSession = Depends(get_session)
):
    # 인증 체크
    if not request.session.get("admin_logged_in"):
        return RedirectResponse(url="/admin/login", status_code=303)
    per_page = 20
    offset = (page - 1) * per_page

    query = select(Post).options(
        selectinload(Post.author),
        selectinload(Post.category)
    )

    if search:
        query = query.where(Post.title.contains(search) | Post.content.contains(search))

    query = query.order_by(desc(Post.created_at)).offset(offset).limit(per_page)

    result = await session.execute(query)
    posts = result.scalars().all()

    return templates.TemplateResponse("admin/posts.html", {
        "request": request,
        "posts": posts,
        "current_page": page,
        "search_query": search
    })

# 게시물 삭제
@router.post("/posts/{post_id}/delete")
async def admin_delete_post(
    request: Request,
    post_id: int,
    session: AsyncSession = Depends(get_session)
):
    # 인증 체크
    if not request.session.get("admin_logged_in"):
        return RedirectResponse(url="/admin/login", status_code=303)
    post_result = await session.execute(select(Post).where(Post.id == post_id))
    post = post_result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=404, detail="게시물을 찾을 수 없습니다.")

    await session.delete(post)
    await session.commit()

    return RedirectResponse(url="/admin/posts", status_code=303)

# 카테고리 관리
@router.get("/categories", response_class=HTMLResponse)
async def admin_categories(
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    # 인증 체크
    if not request.session.get("admin_logged_in"):
        return RedirectResponse(url="/admin/login", status_code=303)
    categories_result = await session.execute(select(Category).order_by(Category.name))
    categories = categories_result.scalars().all()

    return templates.TemplateResponse("admin/categories.html", {
        "request": request,
        "categories": categories
    })

# 카테고리 추가
@router.post("/categories/add")
async def admin_add_category(
    request: Request,
    name: str = Form(...),
    description: Optional[str] = Form(None),
    session: AsyncSession = Depends(get_session)
):
    # 인증 체크
    if not request.session.get("admin_logged_in"):
        return RedirectResponse(url="/admin/login", status_code=303)
    new_category = Category(name=name, description=description)
    session.add(new_category)
    await session.commit()

    return RedirectResponse(url="/admin/categories", status_code=303)

# 카테고리 삭제
@router.post("/categories/{category_id}/delete")
async def admin_delete_category(
    request: Request,
    category_id: int,
    session: AsyncSession = Depends(get_session)
):
    # 인증 체크
    if not request.session.get("admin_logged_in"):
        return RedirectResponse(url="/admin/login", status_code=303)
    category_result = await session.execute(select(Category).where(Category.id == category_id))
    category = category_result.scalar_one_or_none()

    if not category:
        raise HTTPException(status_code=404, detail="카테고리를 찾을 수 없습니다.")

    await session.delete(category)
    await session.commit()

    return RedirectResponse(url="/admin/categories", status_code=303)

# 사용자 관리
@router.get("/users", response_class=HTMLResponse)
async def admin_users(
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    # 인증 체크
    if not request.session.get("admin_logged_in"):
        return RedirectResponse(url="/admin/login", status_code=303)
    users_result = await session.execute(select(UserModel).order_by(UserModel.created_at))
    users = users_result.scalars().all()

    return templates.TemplateResponse("admin/users.html", {
        "request": request,
        "users": users
    })