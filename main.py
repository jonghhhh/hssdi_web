from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.sessions import SessionMiddleware
import os

from app.database import get_session, init_db
from app.routers import admin, dashboard, board

app = FastAPI(
    title="인문·사회과학 데이터 연구소 (HSSDI)",
    description="Humanity & Social Science Data Institute Website",
    version="1.0.0"
)



# 세션 미들웨어 추가
app.add_middleware(SessionMiddleware, secret_key="hssdi-admin-secret-key-2025")

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# 관리자 인증 함수
def check_admin_session(request: Request):
    if not request.session.get("admin_logged_in"):
        return RedirectResponse(url="/admin/login", status_code=303)
    return True

# 관리자 로그인 페이지
@app.get("/admin/login", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    # 이미 로그인되어 있으면 대시보드로 리다이렉트
    if request.session.get("admin_logged_in"):
        return RedirectResponse(url="/crudadmin", status_code=303)
    return templates.TemplateResponse("admin/login.html", {"request": request})

# 관리자 로그인 처리
@app.post("/admin/login")
async def admin_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    # 간단한 SHA256 해시 검증
    import hashlib
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    expected_hash = hashlib.sha256("admin123".encode()).hexdigest()

    if username == "admin" and password_hash == expected_hash:
        request.session["admin_logged_in"] = True
        request.session["admin_username"] = username
        return RedirectResponse(url="/crudadmin", status_code=303)
    else:
        # 로그인 실패 시 에러 메시지와 함께 로그인 페이지로
        return templates.TemplateResponse("admin/login.html", {
            "request": request,
            "error": "사용자명 또는 비밀번호가 올바르지 않습니다."
        })

# 관리자 로그아웃
@app.get("/admin/logout")
async def admin_logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/admin/login", status_code=303)

# Include routers
app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
app.include_router(board.router, prefix="/board", tags=["board"])

# Simple admin interface instead of complex CRUDAdmin
@app.get("/crudadmin", response_class=HTMLResponse)
async def admin_interface(
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    # 인증 체크
    if not request.session.get("admin_logged_in"):
        return RedirectResponse(url="/admin/login", status_code=303)
    from sqlalchemy import select, func
    from app.models import Post, Category, User
    from sqlalchemy.orm import selectinload

    # 통계 데이터 조회
    posts_count = await session.scalar(select(func.count(Post.id)))
    categories_count = await session.scalar(select(func.count(Category.id)))
    users_count = await session.scalar(select(func.count(User.id)))

    # 최근 게시물
    recent_posts_result = await session.execute(
        select(Post).options(
            selectinload(Post.author),
            selectinload(Post.category)
        ).order_by(Post.created_at.desc()).limit(5)
    )
    recent_posts = recent_posts_result.scalars().all()

    return templates.TemplateResponse("admin/admin.html", {
        "request": request,
        "posts_count": posts_count,
        "categories_count": categories_count,
        "users_count": users_count,
        "recent_posts": recent_posts
    })

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/education", response_class=HTMLResponse)
async def education(request: Request):
    return templates.TemplateResponse("education.html", {"request": request})

@app.get("/data-provision", response_class=HTMLResponse)
async def data_provision(request: Request):
    return templates.TemplateResponse("data_provision.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)