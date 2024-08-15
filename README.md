---

# 텍스트 기반 RPG 게임

이 프로젝트는 텍스트 기반의 RPG 게임을 구현한 것입니다. 사용자는 캐릭터를 선택하고, 전투를 수행하며, 아이템을 사용하고, 상점에서 아이템을 구매할 수 있습니다. 이 게임은 Flask 웹 프레임워크를 사용하여 서버 사이드 로직을 처리하며, HTML과 CSS를 사용하여 프론트엔드를 구성합니다.

## 기능

- **캐릭터 선택**: 다양한 캐릭터 중에서 선택할 수 있습니다.
- **전투 시스템**: 적과의 전투에서 공격과 방어를 수행할 수 있습니다.
- **아이템 사용**: 체력 회복 및 공격력 증가 등 다양한 아이템을 사용 가능합니다.
- **상점**: 상점에서 아이템을 구매하고 인벤토리에 추가할 수 있습니다.
- **게임 결과**: 전투 승패에 따른 결과와 경험치 및 골드 보상을 확인할 수 있습니다.

## 설치 및 실행

### 요구 사항

- Python 3.x
- Flask

### 설치

1. **리포지토리 클론**:

   ```bash
   git clone https://github.com/sonenhur/textRPG.git
   cd textRPG
   ```

2. **가상 환경 설정** (선택 사항):

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **필요한 패키지 설치**:

   ```bash
   pip install Flask
   ```

### 실행

1. **Flask 애플리케이션 실행**:

   ```bash
   flask run
   ```

   서버가 `http://127.0.0.1:5000`에서 실행됩니다.

2. **브라우저에서 애플리케이션 열기**:

   웹 브라우저를 열고 `http://127.0.0.1:5000`으로 이동하여 게임을 플레이합니다.

## 프로젝트 디렉토리 구조

```plaintext
textRPG/
├── app.py                        # Flask 애플리케이션의 메인 파일
├── character.py                  # Character 클래스 및 관련 로직
├── items.py                      # Item 클래스 및 아이템 관련 로직
├── quest.py                      # Quest 클래스 및 퀘스트 관련 로직
├── templates/                    # HTML 템플릿 파일들이 위치한 디렉토리
│   ├── base.html                 # 공통 레이아웃 템플릿
│   ├── index.html                # 메인 화면 템플릿
│   ├── character_selection.html  # 캐릭터 선택 화면 템플릿
│   ├── battle.html               # 전투 화면 템플릿
│   ├── inventory.html            # 인벤토리 표시 템플릿
│   └── shop.html                 # 상점 화면 템플릿
├── static/                       # 정적 파일 (CSS, JS, 이미지 등)
│   └── styles.css                # 메인 스타일시트
├── README.md                     # 프로젝트 설명 파일
└── requirements.txt              # 프로젝트 종속성 목록

---
