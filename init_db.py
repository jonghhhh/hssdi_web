#!/usr/bin/env python3

import asyncio
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import engine, Base, SessionLocal
from app.models import User, Category, Research, News, Post
from app.auth import get_password_hash
from app.config import settings

def create_tables_sync():
    Base.metadata.create_all(bind=engine)

def create_sample_data_sync():
    session: Session = SessionLocal()
    try:
        # Check if data already exists
        if session.query(User).count() > 0:
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
        session.flush()

        # 연구진 계정 생성
        director = User(
            username="director",
            email="lee.hoon@kyunghee.ac.kr",
            full_name="이훈 (소장)",
            hashed_password=get_password_hash("director123"),
            is_admin=True,
            is_active=True
        )
        session.add(director)

        research_prof = User(
            username="researcher",
            email="lee.moonhyeok@kyunghee.ac.kr",
            full_name="이문혁 (학술연구교수)",
            hashed_password=get_password_hash("researcher123"),
            is_admin=False,
            is_active=True
        )
        session.add(research_prof)
        session.flush()

        # 카테고리 생성
        categories = [
            Category(name="연구 성과", description="연구소에서 수행한 연구 프로젝트의 결과 및 성과 발표"),
            Category(name="학술 논문", description="연구원들이 게재한 학술 논문 및 연구 보고서"),
            Category(name="공지사항", description="연구소 운영 관련 공지 및 중요 안내사항"),
            Category(name="데이터셋", description="수집 및 가공된 데이터셋 공유 및 활용 안내"),
            Category(name="교육 자료", description="데이터 리터러시 교육 관련 자료 및 튜토리얼"),
            Category(name="ATLAS 시스템", description="ATLAS 시스템 업데이트 및 활용 가이드")
        ]
        session.add_all(categories)
        session.flush()

        # 게시물 등 다른 데이터 추가...
        # (생략된 다른 데이터 추가 로직)

        session.commit()
        print("✅ 데이터베이스 초기 데이터 생성 완료!")
        return True

    except Exception as e:
        session.rollback()
        print(f"❌ 초기 데이터 생성 실패: {e}")
        return False
    finally:
        session.close()

def main():
    print("🔧 데이터베이스 테이블 생성 중...")
    create_tables_sync()
    print("✅ 데이터베이스 테이블 생성 완료!")

    print("📊 초기 데이터 생성 중...")
    success = create_sample_data_sync()

    if success:
        print("\n🎉 데이터베이스 초기화 완료!")
    else:
        print("❌ 데이터베이스 초기화 실패!")

if __name__ == "__main__":
    main()
