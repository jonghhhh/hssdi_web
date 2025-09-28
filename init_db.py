#!/usr/bin/env python3

import asyncio
from sqlalchemy import text
from app.database import create_tables, get_session, SessionLocal
from app.models import User, Category, Research, News, Post
from app.auth import get_password_hash
from app.config import settings

async def create_sample_data():
    async with SessionLocal() as session:
        try:
            # Check if data already exists
            result = await session.execute(text("SELECT 1 FROM users LIMIT 1"))
            if result.scalar_one_or_none():
                print("✅ 데이터가 이미 존재합니다. 초기화를 건너뜁니다.")
                return True

            # 기본 관리자 계정 생성
            admin_user = User(
                username=settings.admin_username,
                email="admin@hssdi.kyunghee.ac.kr",
                full_name="관리자",
                hashed_password=get_password_hash(settings.admin_password),
                is_admin=True,
                is_active=True
            )
            session.add(admin_user)
            await session.flush()

            # 기본 카테고리 생성
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
            await session.flush()

            # 샘플 연구 데이터 생성
            sample_research = [
                Research(
                    title="AI 기반 텍스트 마이닝 연구",
                    description="자연어 처리를 통한 인문학 텍스트 분석",
                    research_type="인공지능",
                    status="진행중"
                ),
                Research(
                    title="디지털 인문학 플랫폼 구축",
                    description="웹 기반 인문학 연구 플랫폼 개발",
                    research_type="플랫폼",
                    status="계획"
                ),
                Research(
                    title="소셜 네트워크 분석 연구",
                    description="온라인 커뮤니티의 사회적 관계 분석",
                    research_type="소셜네트워크",
                    status="완료"
                )
            ]

            for research in sample_research:
                session.add(research)
            await session.flush()

            # 샘플 뉴스 생성
            sample_news = [
                News(
                    title="연구소 개설 기념 학술대회 개최",
                    content="2025년 9월 인문·사회과학 데이터 연구소 개설을 기념하는 학술대회를 개최합니다.",
                    author_id=admin_user.id,
                    is_featured=True
                ),
                News(
                    title="데이터 과학 워크숍 참가자 모집",
                    content="연구자를 위한 데이터 과학 기초 워크숍 참가자를 모집합니다.",
                    author_id=admin_user.id,
                    is_featured=True
                ),
                News(
                    title="협력 연구기관 네트워크 확장",
                    content="국내외 유수 대학과의 협력 연구 네트워크를 확장합니다.",
                    author_id=admin_user.id,
                    is_featured=False
                )
            ]

            for news in sample_news:
                session.add(news)
            await session.flush()

            # 샘플 게시물 생성
            sample_posts = [
                Post(
                    title="인문·사회과학 데이터 연구소 개설 안내",
                    content="경희대학교 부설 인문·사회과학 데이터 연구소가 2025년 8월 28일 개설되었습니다. 본 연구소는 인문학과 사회과학 분야의 데이터 기반 연구를 지원하고, 디지털 인문학 연구 방법론을 개발하는 것을 목표로 합니다.",
                    author_id=admin_user.id,
                    category_id=1,
                    is_published=True
                ),
                Post(
                    title="AI 기반 데이터 분석 워크숍 개최",
                    content="연구자들을 위한 AI 기반 데이터 분석 워크숍을 개최합니다. 본 워크숍에서는 기초적인 데이터 분석부터 고급 머신러닝 기법까지 다룰 예정입니다.",
                    author_id=admin_user.id,
                    category_id=4,
                    is_published=True
                ),
                Post(
                    title="2025년 연구 협력 네트워크 구축 사업",
                    content="국내외 연구기관과의 협력 네트워크 구축을 위한 사업을 시작합니다. 관심 있는 연구자들의 많은 참여 바랍니다.",
                    author_id=admin_user.id,
                    category_id=6,
                    is_published=True
                ),
                Post(
                    title="디지털 인문학 연구 방법론 세미나",
                    content="디지털 시대의 인문학 연구 방법론에 대한 세미나를 개최합니다. 최신 연구 동향과 실습을 통해 디지털 인문학의 이해를 높이고자 합니다.",
                    author_id=admin_user.id,
                    category_id=3,
                    is_published=True
                ),
                Post(
                    title="연구 데이터 관리 가이드라인",
                    content="효과적인 연구 데이터 관리를 위한 가이드라인을 제공합니다. 데이터의 수집, 저장, 분석, 공유에 대한 모범 사례를 소개합니다.",
                    author_id=admin_user.id,
                    category_id=5,
                    is_published=True
                )
            ]

            for post in sample_posts:
                session.add(post)

            await session.commit()
            print("✅ 데이터베이스 초기 데이터 생성 완료!")
            return True

        except Exception as e:
            await session.rollback()
            print(f"❌ 초기 데이터 생성 실패: {e}")
            # In case of partial table creation, etc.
            # It might be better to raise the exception to fail the build.
            raise e
        finally:
            await session.close()

async def main():
    print("🔧 데이터베이스 테이블 생성 중...")
    await create_tables()
    print("✅ 데이터베이스 테이블 생성 완료!")

    print("📊 초기 데이터 생성 중...")
    success = await create_sample_data()

    if success:
        print("\n🎉 데이터베이스 초기화 완료!")
    else:
        print("❌ 데이터베이스 초기화 실패!")

if __name__ == "__main__":
    # This allows running the script directly to initialize the database.
    # The build script on Render will execute this.
    asyncio.run(main())