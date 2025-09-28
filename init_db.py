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

            # (이하 샘플 데이터 추가 로직은 원본과 동일하게 유지)
            # ...

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