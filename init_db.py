#!/usr/bin/env python3

import asyncio
from sqlalchemy import text
from app.database import create_tables, get_session
from app.models import User, Category, Research, News, Post
from app.auth import get_password_hash
from app.config import settings

async def create_sample_data():
    async for session in get_session():
        try:
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
            await session.flush()

            # 카테고리 생성
            categories = [
                Category(
                    name="연구 성과",
                    description="연구소에서 수행한 연구 프로젝트의 결과 및 성과 발표"
                ),
                Category(
                    name="학술 논문",
                    description="연구원들이 게재한 학술 논문 및 연구 보고서"
                ),
                Category(
                    name="공지사항",
                    description="연구소 운영 관련 공지 및 중요 안내사항"
                ),
                Category(
                    name="데이터셋",
                    description="수집 및 가공된 데이터셋 공유 및 활용 안내"
                ),
                Category(
                    name="교육 자료",
                    description="데이터 리터러시 교육 관련 자료 및 튜토리얼"
                ),
                Category(
                    name="ATLAS 시스템",
                    description="ATLAS 시스템 업데이트 및 활용 가이드"
                )
            ]

            for category in categories:
                session.add(category)
            await session.flush()

            # 연구 프로젝트 생성
            research_projects = [
                Research(
                    title="텍스트 마이닝을 활용한 소셜미디어 여론 분석",
                    description="소셜미디어 빅데이터를 활용하여 정치·사회 이슈에 대한 국민 여론의 변화 패턴을 분석하고 예측하는 연구",
                    research_type="텍스트 및 음성 분석",
                    status="진행중"
                ),
                Research(
                    title="AI 기반 가짜뉴스 탐지 시스템 개발",
                    description="자연어 처리와 딥러닝 기술을 활용하여 가짜뉴스를 자동으로 탐지하고 분류하는 시스템 구축",
                    research_type="AI 기반 정책 연구",
                    status="진행중"
                ),
                Research(
                    title="영상 콘텐츠 기반 사회 현상 분석",
                    description="유튜브, 틱톡 등 영상 플랫폼의 콘텐츠 분석을 통한 사회 트렌드 및 문화 변화 연구",
                    research_type="영상 및 이미지 분석",
                    status="계획"
                ),
                Research(
                    title="정형 데이터 기반 정책 효과 측정",
                    description="정부 정책의 효과를 정량적으로 측정하고 평가하기 위한 데이터 분석 모델 개발",
                    research_type="정형 데이터 분석",
                    status="진행중"
                ),
                Research(
                    title="데이터 리터러시 교육 효과성 연구",
                    description="데이터 활용 교육 프로그램의 효과성을 측정하고 개선 방안을 도출하는 연구",
                    research_type="교육 및 협력",
                    status="완료"
                )
            ]

            for research in research_projects:
                session.add(research)
            await session.flush()

            # 뉴스 생성
            news_items = [
                News(
                    title="인문·사회과학 데이터 연구소 공식 개소",
                    content="경희대학교 부설 인문·사회과학 데이터 연구소(HSSDI)가 2025년 8월 28일 공식 개소했습니다. 이훈 소장을 중심으로 5개 연구팀이 구성되어 데이터 기반 사회문제 해결 연구에 본격 착수할 예정입니다.",
                    author_id=director.id,
                    is_featured=True
                ),
                News(
                    title="ATLAS 시스템 베타 버전 출시",
                    content="AI Technology for Live Analysis of Social data(ATLAS) 시스템의 베타 버전이 출시되었습니다. 실시간 소셜미디어 데이터 분석과 시각화 기능을 제공합니다.",
                    author_id=research_prof.id,
                    is_featured=True
                ),
                News(
                    title="데이터 리터러시 교육 프로그램 개시",
                    content="연구자 및 정책 입안자를 대상으로 하는 데이터 리터러시 교육 프로그램이 시작됩니다. AI 및 빅데이터 분석 방법론을 체계적으로 학습할 수 있습니다.",
                    author_id=admin_user.id,
                    is_featured=False
                )
            ]

            for news in news_items:
                session.add(news)
            await session.flush()

            # 게시물 생성
            posts = [
                Post(
                    title="연구소 개소 인사말",
                    content="""안녕하세요. 인문·사회과학 데이터 연구소 소장 이훈입니다.

경희대학교 부설 인문·사회과학 데이터 연구소(HSSDI)의 공식 개소를 알려드립니다.

## 연구소 비전

우리 연구소는 데이터 기반 연구를 통해 사회가 직면한 복합적 문제를 해결하고, 이를 선도하는 연구 허브가 되는 것을 목적으로 합니다.

## 주요 연구 분야

- 텍스트 및 음성 분석
- 영상 및 이미지 분석
- 정형 데이터 분석
- AI 기반 정책 연구
- 교육 및 협력

앞으로 많은 관심과 협력 부탁드립니다.

감사합니다.""",
                    author_id=director.id,
                    category_id=categories[2].id,  # 공지사항
                    is_published=True
                ),
                Post(
                    title="ATLAS 시스템 소개 및 활용 가이드",
                    content="""# ATLAS 시스템 개요

**ATLAS (AI Technology for Live Analysis of Social data)**는 우리 연구소의 핵심 분석 시스템입니다.

## 시스템 구성

### 1. 데이터 수집 레이어
- 미디어 데이터 (뉴스, 소셜미디어)
- 공공 데이터 (정부 보도자료, 통계)
- 정책 데이터 (법안, 정책 논의)
- 경제 데이터 (지표, 금융 정보)

### 2. AI 분석 처리 레이어
- 실시간 데이터 수집
- LangGraph 에이전트 시스템
- LLM 분석 엔진
- 구조화된 데이터 저장

### 3. 서비스 제공 레이어
- Streamlit 대시보드
- API 서비스
- 교육 서비스

자세한 활용법은 곧 업데이트될 예정입니다.""",
                    author_id=research_prof.id,
                    category_id=categories[5].id,  # ATLAS 시스템
                    is_published=True
                ),
                Post(
                    title="데이터 윤리 및 AI 공정성 연구 가이드라인",
                    content="""# 연구 윤리 가이드라인

## 데이터 수집 및 처리 원칙

### 1. 개인정보 보호
- 개인식별정보 제거 및 익명화
- GDPR 및 개인정보보호법 준수
- 데이터 최소화 원칙 적용

### 2. AI 공정성 확보
- 편향 데이터 탐지 및 제거
- 다양성을 고려한 데이터셋 구성
- 알고리즘 투명성 확보

### 3. 연구 투명성
- 연구 방법론 공개
- 데이터 출처 명시
- 한계점 명확히 기술

모든 연구는 이러한 원칙 하에 수행되어야 합니다.""",
                    author_id=admin_user.id,
                    category_id=categories[0].id,  # 연구 성과
                    is_published=True
                )
            ]

            for post in posts:
                session.add(post)

            await session.commit()
            print("✅ 데이터베이스 초기 데이터 생성 완료!")
            return True

        except Exception as e:
            await session.rollback()
            print(f"❌ 초기 데이터 생성 실패: {e}")
            return False
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
        print("\n📋 생성된 계정 정보:")
        print(f"   관리자: {settings.admin_username} / {settings.admin_password}")
        print("   소장: director / director123")
        print("   연구교수: researcher / researcher123")
        print("\n🌐 웹사이트 접속 방법:")
        print("   1. 가상환경 활성화: source .venv/bin/activate")
        print("   2. 패키지 설치: pip install -r requirements.txt")
        print("   3. 서버 실행: python main.py")
        print("   4. 브라우저에서 http://localhost:8000 접속")
        print("\n🔧 관리자 패널: http://localhost:8000/crudadmin")
    else:
        print("❌ 데이터베이스 초기화 실패!")

if __name__ == "__main__":
    asyncio.run(main())