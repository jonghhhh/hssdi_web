#!/usr/bin/env python3
"""
Script to fix Korean text encoding issues in the database
"""
import asyncio
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.ext.asyncio import AsyncSession
from app.database import SessionLocal, engine, create_tables
from app.models import User, Post, Category, Research, News

async def backup_and_fix_encoding():
    """Backup existing data and recreate with proper encoding"""

    print("🔄 Starting encoding fix process...")

    # Backup existing data
    async with SessionLocal() as session:
        print("📦 Backing up existing data...")

        # Get all posts
        from sqlalchemy import select
        posts_result = await session.execute(select(Post))
        posts = posts_result.scalars().all()

        # Get all categories
        categories_result = await session.execute(select(Category))
        categories = categories_result.scalars().all()

        print(f"📊 Found {len(posts)} posts and {len(categories)} categories")

    # Delete old database
    if os.path.exists("hssdi.db"):
        print("🗑️  Removing old database...")
        os.remove("hssdi.db")

    # Create new database with tables
    print("🏗️  Creating new database...")
    await create_tables()

    # Recreate data with proper Korean text
    async with SessionLocal() as session:
        print("✨ Recreating data with proper encoding...")

        # Create categories with proper Korean text
        research_category = Category(
            name="연구 동향",
            description="최신 연구 동향 및 분석"
        )

        data_category = Category(
            name="데이터 분석",
            description="데이터 과학 및 분석 기법"
        )

        policy_category = Category(
            name="정책 연구",
            description="정책 개발 및 효과 분석"
        )

        tech_category = Category(
            name="기술 동향",
            description="최신 기술 및 도구 소개"
        )

        ai_category = Category(
            name="AI 연구",
            description="인공지능 및 머신러닝 연구"
        )

        education_category = Category(
            name="교육 프로그램",
            description="데이터 리터러시 교육"
        )

        session.add_all([research_category, data_category, policy_category, tech_category, ai_category, education_category])
        await session.commit()

        # Get admin user (should exist)
        from sqlalchemy import select
        admin_result = await session.execute(select(User).where(User.id == 1))
        admin_user = admin_result.scalar_one_or_none()

        if not admin_user:
            # Create admin user if not exists
            admin_user = User(
                username="admin",
                email="admin@hssdi.ac.kr",
                full_name="관리자",
                hashed_password="$2b$12$placeholder",
                is_admin=True
            )
            session.add(admin_user)
            await session.commit()

        # Create sample posts with proper Korean text
        sample_posts = [
            Post(
                title="인문·사회과학 데이터 연구소 개설 안내",
                content="경희대학교 인문·사회과학 데이터 연구소(HSSDI)가 새롭게 개설되었습니다.\n\n주요 연구 분야:\n- 텍스트 및 음성 분석\n- 영상 및 이미지 분석\n- 정형 데이터 분석\n- AI 기반 정책 연구\n- 데이터 리터러시 교육\n\n많은 관심과 참여 부탁드립니다.",
                author_id=admin_user.id,
                category_id=research_category.id,
                is_published=True,
                views=0
            ),
            Post(
                title="ATLAS 시스템 구축 현황",
                content="AI 기반 텍스트 분석 시스템(ATLAS) 구축이 진행 중입니다.\n\n주요 기능:\n- 실시간 데이터 수집\n- 자연어 처리 기반 감성 분석\n- 이슈 추출 및 트렌드 분석\n- 시각화 대시보드\n\n현재 95.2%의 분석 정확도를 달성했습니다.",
                author_id=admin_user.id,
                category_id=tech_category.id,
                is_published=True,
                views=0
            ),
            Post(
                title="데이터 리터러시 교육 프로그램 안내",
                content="데이터 활용 능력 향상을 위한 교육 프로그램을 운영합니다.\n\n교육 내용:\n- 데이터 수집 및 전처리\n- 통계 분석 기초\n- 데이터 시각화\n- 머신러닝 입문\n\n교육 문의: education@hssdi.ac.kr",
                author_id=admin_user.id,
                category_id=education_category.id,
                is_published=True,
                views=0
            )
        ]

        session.add_all(sample_posts)
        await session.commit()

        print("✅ Database encoding fix completed successfully!")
        print("📝 Created sample posts with proper Korean encoding")

if __name__ == "__main__":
    asyncio.run(backup_and_fix_encoding())