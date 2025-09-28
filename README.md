# 인문·사회과학 데이터 연구소 (HSSDI) 웹사이트

경희대학교 부설 인문·사회과학 데이터 연구소의 공식 웹사이트입니다.

## 📋 프로젝트 개요

- **연구소명**: 인문·사회과학 데이터 연구소 (Humanity & Social Science Data Institute, HSSDI)
- **설립일**: 2025년 8월 28일
- **소장**: 이훈 (미디어학과 교수)
- **학술연구교수**: 이문혁
- **위치**: 경희대학교 제2법학관 1층

## 🏗️ 시스템 구조

### 백엔드
- **FastAPI**: 고성능 Python 웹 프레임워크
- **SQLAlchemy**: 비동기 ORM
- **PostgreSQL/SQLite**: 데이터베이스
- **FastCRUD**: 관리자 패널 (CRUDAdmin 기반)
- **JWT**: 인증 시스템

### 프론트엔드
- **Jinja2**: 템플릿 엔진
- **CSS3**: 경희대 브랜드 색상 적용
- **JavaScript**: 인터랙티브 기능

## 🚀 설치 및 실행

### 1. 의존성 설치

```bash
# 가상환경 활성화 (이미 생성되어 있는 경우)
source ../.venv/bin/activate

# 패키지 설치
pip install -r requirements.txt
```

### 2. 데이터베이스 초기화

```bash
# 데이터베이스 테이블 생성 및 초기 데이터 입력
python init_db.py
```

### 3. 서버 실행

```bash
# 개발 서버 실행
python main.py

# 또는
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. 웹사이트 접속

- **메인 사이트**: http://localhost:8000
- **대시보드**: http://localhost:8000/dashboard
- **게시판**: http://localhost:8000/board
- **관리자 패널**: http://localhost:8000/crudadmin

## 👥 기본 계정 정보

데이터베이스 초기화 후 다음 계정들이 생성됩니다:

| 역할 | 사용자명 | 비밀번호 | 권한 |
|------|----------|----------|------|
| 관리자 | admin | admin123 | 전체 관리 |
| 소장 | director | director123 | 관리자 |
| 연구교수 | researcher | researcher123 | 일반 사용자 |

## 📁 프로젝트 구조

```
hssdi_web/
├── app/
│   ├── __init__.py
│   ├── config.py          # 설정 파일
│   ├── database.py        # 데이터베이스 연결
│   ├── models.py          # 데이터 모델
│   ├── schemas.py         # Pydantic 스키마
│   ├── auth.py           # 인증 시스템
│   ├── admin_setup.py    # 관리자 패널 설정
│   └── routers/          # API 라우터
│       ├── admin.py
│       ├── dashboard.py
│       └── board.py
├── templates/            # HTML 템플릿
│   ├── base.html
│   ├── index.html
│   ├── about.html
│   ├── dashboard/
│   └── board/
├── static/              # 정적 파일
│   ├── css/
│   ├── js/
│   └── images/
├── main.py             # 메인 애플리케이션
├── init_db.py          # 데이터베이스 초기화
├── requirements.txt    # 의존성 목록
└── README.md
```

## 🎨 디자인 시스템

### 색상 팔레트 (경희대학교 브랜드)
- **주색상**: `#8B4513` (진한 갈색)
- **보조색상**: `#DC143C` (진한 빨간색)
- **강조색상**: `#A0522D` (중간 갈색)
- **연한색상**: `#DEB887` (연한 갈색)

### 타이포그래피
- **폰트**: Noto Sans KR
- **제목**: 700 (Bold)
- **본문**: 400 (Regular)

## 🔧 주요 기능

### 1. 홈페이지
- 연구소 소개
- 주요 연구 분야 안내
- ATLAS 시스템 소개
- 연구팀 정보

### 2. 대시보드
- 실시간 통계 (게시물, 연구, 뉴스, 사용자)
- 최근 게시물 목록
- 진행 중인 연구 현황
- 주요 뉴스

### 3. 게시판
- 게시물 CRUD (생성, 읽기, 수정, 삭제)
- 카테고리 분류
- 검색 기능
- 페이지네이션
- 조회수 카운팅

### 4. 관리자 패널
- 사용자 관리
- 게시물 관리
- 카테고리 관리
- 연구 프로젝트 관리
- 뉴스 관리

## 📊 연구팀 구성

1. **텍스트 및 음성 분석팀**
   - 자연어 처리, 감성 분석, 음성 인식

2. **영상 및 이미지 분석팀**
   - 컴퓨터 비전, 딥러닝, 패턴 인식

3. **정형 데이터 분석팀**
   - 통계 분석, 머신러닝, 예측 모델링

4. **AI 기반 정책 연구팀**
   - 정책 효과 분석, AI 기반 정책 제안

5. **교육 및 협력팀**
   - 데이터 리터러시 교육, 국제 협력

## 🔒 보안 기능

- JWT 기반 인증 시스템
- 비밀번호 해싱 (bcrypt)
- CORS 설정
- SQL Injection 방지
- XSS 방지

## 🌐 API 엔드포인트

### 인증
- `POST /admin/login` - 관리자 로그인
- `GET /admin/me` - 현재 사용자 정보

### 대시보드
- `GET /dashboard/` - 대시보드 메인
- `GET /dashboard/analytics` - 분석 리포트
- `GET /dashboard/research` - 연구 현황

### 게시판
- `GET /board/` - 게시물 목록
- `GET /board/{id}` - 게시물 상세
- `POST /board/create` - 게시물 작성
- `PUT /board/{id}/edit` - 게시물 수정
- `DELETE /board/{id}/delete` - 게시물 삭제

## 📝 개발 가이드

### 새로운 기능 추가
1. 모델 정의 (`app/models.py`)
2. 스키마 작성 (`app/schemas.py`)
3. 라우터 구현 (`app/routers/`)
4. 템플릿 작성 (`templates/`)
5. 스타일 적용 (`static/css/`)

### 데이터베이스 마이그레이션
```bash
# Alembic 초기화 (필요시)
alembic init alembic

# 마이그레이션 파일 생성
alembic revision --autogenerate -m "Add new table"

# 마이그레이션 적용
alembic upgrade head
```

## 🤝 기여 가이드

1. 이슈 생성 또는 기존 이슈 확인
2. 브랜치 생성 (`feature/기능명` 또는 `fix/버그명`)
3. 코드 작성 및 테스트
4. 커밋 메시지 작성 (한글 가능)
5. Pull Request 생성

## 📞 연락처

- **연구소 소장**: 이훈 (lee.hoon@kyunghee.ac.kr)
- **학술연구교수**: 이문혁 (lee.moonhyeok@kyunghee.ac.kr)
- **기술 문의**: admin@hssdi.kyunghee.ac.kr

## 📄 라이선스

Copyright © 2025 경희대학교 인문·사회과학 데이터 연구소. All rights reserved.

---

**인문·사회과학 데이터 연구소 (HSSDI)**
경희대학교 제2법학관 1층
서울특별시 동대문구 경희대로 26