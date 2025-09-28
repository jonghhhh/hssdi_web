from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.config import settings
from app.db_base import Base # Import Base from the new central file

engine = create_async_engine(
    settings.database_url,
    echo=True,
    future=True
)

SessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def init_db():
    """데이터베이스 테이블 생성 및 초기 데이터 입력"""
    # Models are imported here, within the function scope, to be used.
    from app.models import User, Category, Post
    from sqlalchemy import select
    import asyncio

    # 테이블 생성
    await create_tables()

    # 세션 생성
    async with SessionLocal() as session:
        # 기본 관리자 계정 확인
        result = await session.execute(select(User).where(User.username == "admin"))
        admin_user = result.scalar_one_or_none()

        if not admin_user:
            import hashlib

            # 관리자 계정 생성 (간단한 SHA256 해시 사용)
            password_hash = hashlib.sha256("admin123".encode()).hexdigest()
            admin_user = User(
                username="admin",
                email="admin@hssdi.ac.kr",
                full_name="관리자",
                hashed_password=password_hash,
                is_admin=True,
                is_active=True
            )
            session.add(admin_user)
            await session.commit()
            await session.refresh(admin_user)

        # 기본 카테고리 확인
        result = await session.execute(select(Category))
        categories = result.scalars().all()

        if not categories:
            default_categories = [
                Category(name="공지사항", description="연구소 공지사항"),
                Category(name="연구소식", description="연구 관련 소식"),
                Category(name="학술행사", description="학술 행사 및 세미나"),
                Category(name="교육프로그램", description="교육 프로그램 안내"),
                Category(name="자료실", description="연구 자료 및 문서"),
                Category(name="협력기관", description="협력기관 소식")
            ]

            for category in default_categories:
                session.add(category)

            await session.commit()

            # 샘플 게시물 생성
            sample_posts = [
                Post(
                    title="인문·사회과학 데이터 연구소 개설 안내",
                    content="경희대학교 부설 인문·사회과학 데이터 연구소가 2025년 8월 28일 개설되었습니다.",
                    author_id=admin_user.id,
                    category_id=1,
                    is_published=True
                ),
                Post(
                    title="AI 기반 데이터 분석 워크숍 개최",
                    content="연구자들을 위한 AI 기반 데이터 분석 워크숍을 개최합니다.",
                    author_id=admin_user.id,
                    category_id=4,
                    is_published=True
                ),
                Post(
                    title="2025년 연구 협력 네트워크 구축 사업",
                    content="국내외 연구기관과의 협력 네트워크 구축을 위한 사업을 시작합니다.",
                    author_id=admin_user.id,
                    category_id=6,
                    is_published=True
                )
            ]

            for post in sample_posts:
                session.add(post)

            await session.commit()