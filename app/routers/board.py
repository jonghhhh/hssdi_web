from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload
from typing import Optional

from app.database import get_session
from app.models import Post, Category, User
from app.schemas import PostCreate, PostUpdate
from app.auth import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def board_list(
    request: Request,
    page: int = 1,
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    session: AsyncSession = Depends(get_session)
):
    per_page = 10
    offset = (page - 1) * per_page

    # 기본 쿼리 - eager loading으로 author와 category 미리 로드
    query = select(Post).options(
        selectinload(Post.author),
        selectinload(Post.category)
    ).where(Post.is_published == True)

    # 카테고리 필터
    if category_id:
        query = query.where(Post.category_id == category_id)

    # 검색 필터
    if search:
        query = query.where(Post.title.contains(search) | Post.content.contains(search))

    # 정렬 및 페이징
    query = query.order_by(desc(Post.created_at)).offset(offset).limit(per_page)

    result = await session.execute(query)
    posts = result.scalars().all()

    # 카테고리 목록
    categories_result = await session.execute(select(Category))
    categories = categories_result.scalars().all()

    return templates.TemplateResponse("board/list.html", {
        "request": request,
        "posts": posts,
        "categories": categories,
        "current_page": page,
        "current_category": category_id,
        "search_query": search
    })

@router.get("/create", response_class=HTMLResponse)
async def board_create_form(
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    categories_result = await session.execute(select(Category))
    categories = categories_result.scalars().all()

    return templates.TemplateResponse("board/create.html", {
        "request": request,
        "categories": categories
    })

@router.post("/create")
async def board_create(
    title: str = Form(...),
    content: str = Form(...),
    category_id: Optional[int] = Form(None),
    session: AsyncSession = Depends(get_session)
):
    # 기본 관리자 사용자 (ID: 1)를 작성자로 설정
    new_post = Post(
        title=title,
        content=content,
        category_id=category_id,
        author_id=1  # 기본 관리자 ID
    )
    session.add(new_post)
    await session.commit()
    await session.refresh(new_post)

    return RedirectResponse(url=f"/board/{new_post.id}", status_code=303)

@router.get("/{post_id}", response_class=HTMLResponse)
async def board_detail(
    request: Request,
    post_id: int,
    session: AsyncSession = Depends(get_session)
):
    # 조회수 증가 - eager loading으로 author와 category 미리 로드
    post_result = await session.execute(
        select(Post).options(
            selectinload(Post.author),
            selectinload(Post.category)
        ).where(Post.id == post_id)
    )
    post = post_result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=404, detail="게시물을 찾을 수 없습니다.")

    # 조회수 증가
    post.views += 1
    await session.commit()

    # 세션을 닫기 전에 모든 필요한 속성을 미리 로드
    await session.refresh(post)

    return templates.TemplateResponse("board/detail.html", {
        "request": request,
        "post": post
    })

@router.get("/{post_id}/edit", response_class=HTMLResponse)
async def board_edit_form(
    request: Request,
    post_id: int,
    session: AsyncSession = Depends(get_session)
):
    post_result = await session.execute(
        select(Post).options(
            selectinload(Post.author),
            selectinload(Post.category)
        ).where(Post.id == post_id)
    )
    post = post_result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=404, detail="게시물을 찾을 수 없습니다.")

    categories_result = await session.execute(select(Category))
    categories = categories_result.scalars().all()

    return templates.TemplateResponse("board/edit.html", {
        "request": request,
        "post": post,
        "categories": categories
    })

@router.post("/{post_id}/edit")
async def board_edit(
    post_id: int,
    title: str = Form(...),
    content: str = Form(...),
    category_id: Optional[int] = Form(None),
    session: AsyncSession = Depends(get_session)
):
    post_result = await session.execute(select(Post).where(Post.id == post_id))
    post = post_result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=404, detail="게시물을 찾을 수 없습니다.")

    post.title = title
    post.content = content
    post.category_id = category_id

    await session.commit()

    return RedirectResponse(url=f"/board/{post_id}", status_code=303)

@router.post("/{post_id}/delete")
async def board_delete(
    post_id: int,
    session: AsyncSession = Depends(get_session)
):
    post_result = await session.execute(select(Post).where(Post.id == post_id))
    post = post_result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=404, detail="게시물을 찾을 수 없습니다.")

    await session.delete(post)
    await session.commit()

    return RedirectResponse(url="/board", status_code=303)