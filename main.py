import streamlit as st
from dataclasses import dataclass
from typing import List, Dict
import random

st.set_page_config(
    page_title="✨ MBTI 진로 추천 랩 🚀",
    page_icon="🧭",
    layout="wide",
)

# -----------------------------
# 🎨 Custom CSS (화려하게)
# -----------------------------
CUSTOM_CSS = """
<style>
/* 전체 배경 그라데이션 */
.stApp {
  background: radial-gradient(circle at 10% 10%, rgba(255,0,150,0.18), transparent 45%),
              radial-gradient(circle at 90% 20%, rgba(0,200,255,0.18), transparent 40%),
              radial-gradient(circle at 30% 90%, rgba(0,255,120,0.16), transparent 45%),
              linear-gradient(135deg, #0b1020 0%, #111a33 35%, #0b1020 100%);
  color: #EAF0FF;
}

/* 기본 텍스트/링크 */
html, body, [class*="css"]  {
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, "Noto Sans KR", "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
}

/* 타이틀 글로우 */
.glow-title {
  font-size: 44px;
  font-weight: 900;
  letter-spacing: -0.5px;
  margin: 0;
  background: linear-gradient(90deg, #ff4fd8, #7a5cff, #3de6ff, #55ff9b);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 0 22px rgba(122,92,255,0.25);
}

/* 서브타이틀 */
.subtitle {
  margin-top: 6px;
  font-size: 16px;
  color: rgba(234, 240, 255, 0.85);
}

/* 유리(Glass) 카드 */
.glass {
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.12);
  box-shadow: 0 12px 40px rgba(0,0,0,0.35);
  border-radius: 18px;
  padding: 18px 18px 14px 18px;
  backdrop-filter: blur(10px);
}

/* 뱃지 */
.badge {
  display:inline-block;
  padding: 6px 10px;
  border-radius: 999px;
  background: rgba(255,255,255,0.10);
  border: 1px solid rgba(255,255,255,0.16);
  margin-right: 6px;
  margin-bottom: 6px;
  font-size: 13px;
}

/* 버튼 스타일 */
div.stButton > button {
  background: linear-gradient(90deg, #ff4fd8 0%, #7a5cff 40%, #3de6ff 75%, #55ff9b 100%);
  color: #0b1020;
  font-weight: 900;
  border: none;
  border-radius: 14px;
  padding: 0.8rem 1.1rem;
  box-shadow: 0 14px 36px rgba(122,92,255,0.25);
}
div.stButton > button:hover {
  filter: brightness(1.05);
  transform: translateY(-1px);
}

/* selectbox/slider 배경 */
[data-baseweb="select"] > div {
  background: rgba(255,255,255,0.06) !important;
  border-radius: 14px !important;
  border: 1px solid rgba(255,255,255,0.12) !important;
}

/* expander */
details summary {
  font-weight: 800 !important;
  color: rgba(234,240,255,0.95) !important;
}

/* 구분선 */
.hr {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.25), transparent);
  margin: 16px 0;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -----------------------------
# 🧩 Data Model
# -----------------------------
@dataclass
class CareerPack:
    tagline: str
    strengths: List[str]
    careers: List[str]
    environments: List[str]
    study_tips: List[str]
    keywords: List[str]

# -----------------------------
# 🧠 MBTI Career Dictionary
# (교육용: 절대적 기준이 아닌 '탐색 가이드'로 구성)
# -----------------------------
MBTI_DATA: Dict[str, CareerPack] = {
    "INTJ": CareerPack(
        tagline="🧠 전략가 모드 ON! 큰 그림 설계 + 장기 플랜에 강함 🏗️✨",
        strengths=["🔭 장기 전략 수립", "🧩 복잡한 문제 구조화", "📈 효율·최적화", "🧪 분석적 사고"],
        careers=["🧠 데이터 사이언티스트", "🧩 전략 컨설턴트", "🏛️ 정책/기획 연구원", "🛠️ 제품 매니저(PM)", "🔐 정보보안 분석가"],
        environments=["📊 목표·지표가 명확한 조직", "🧘 자율성이 높은 업무", "🧱 깊게 파고드는 프로젝트", "🔬 연구/기술 중심 팀"],
        study_tips=["🗺️ 로드맵을 먼저 그리기", "📚 핵심 개념 → 응용 과제 순으로 학습", "🧾 성과지표(포트폴리오)로 증명하기"],
        keywords=["전략", "기획", "분석", "최적화", "연구"]
    ),
    "INTP": CareerPack(
        tagline="🌀 아이디어 공장 가동! 원리·개념 탐구에 진심 🔍💡",
        strengths=["🧠 논리적 탐구", "🧵 개념 연결", "🧪 실험·가설 설정", "🛠️ 문제 해결"],
        careers=["🧑‍💻 소프트웨어 엔지니어", "🧪 R&D 연구원", "📐 알고리즘/AI 엔지니어", "🧠 인지과학/UX 리서처", "🧮 퀀트/리서치 애널리스트"],
        environments=["🧩 새로운 문제를 실험하는 환경", "🧪 시도·실패가 허용되는 문화", "📚 지적 호기심을 존중하는 팀"],
        study_tips=["🧾 개념노트(정리) + 작은 실험(코딩/프로토타입)", "🎯 완벽주의 대신 ‘버전1’ 먼저 만들기", "🧑‍🤝‍🧑 스터디로 마감(데드라인) 확보"],
        keywords=["탐구", "이론", "실험", "창의", "논리"]
    ),
    "ENTJ": CareerPack(
        tagline="👑 리더십 폭발! 목표 달성형 추진력 💥📣",
        strengths=["🚀 실행·추진", "🧭 의사결정", "📊 성과 관리", "🤝 조직 리딩"],
        careers=["📌 사업개발(BD)", "🧩 경영 컨설턴트", "🛠️ 프로덕트 오너", "🏢 조직/운영 매니저", "💼 세일즈 리더"],
        environments=["🎯 목표·성과 중심", "🏁 빠른 속도와 경쟁", "🧑‍🤝‍🧑 역할이 명확한 팀"],
        study_tips=["📈 KPI 기반 포트폴리오 만들기", "🗣️ 발표·협상 스킬 훈련", "🧾 케이스 스터디로 의사결정 근육 키우기"],
        keywords=["리더십", "성과", "전략", "비즈니스", "결정"]
    ),
    "ENTP": CareerPack(
        tagline="🎢 아이디어 롤러코스터! 설득·혁신·도전의 화신 🧨😎",
        strengths=["💡 발상 전환", "🗣️ 설득·토론", "🧪 빠른 프로토타이핑", "🌪️ 변화 적응"],
        careers=["🚀 스타트업 창업", "📣 마케팅/브랜딩", "🎤 크리에이터/방송", "🧩 기획자", "🧑‍⚖️ 변호사/정책 커뮤니케이터"],
        environments=["🌈 자유로운 아이디어 문화", "⚡ 속도감 있는 프로젝트", "🧩 다양한 사람과의 협업"],
        study_tips=["🎬 ‘만들면서 배우기’(프로젝트 기반)", "🧾 토론/피칭 대회 참여", "📅 마감 관리용 캘린더 필수"],
        keywords=["혁신", "토론", "기획", "설득", "창업"]
    ),
    "INFJ": CareerPack(
        tagline="🌙 조용히 강한 이상주의! 사람과 의미에 진심 🕯️💞",
        strengths=["🧭 가치 중심", "🧠 통찰", "🤝 공감·상담", "📝 글/콘텐츠"],
        careers=["🧑‍⚕️ 상담/임상심리", "📚 교육/교사", "🧑‍💼 HR/조직문화", "✍️ 작가/에디터", "🧭 사회혁신/NGO"],
        environments=["🫶 사람을 돕는 미션형 조직", "🧘 집중 가능한 조용한 환경", "📚 깊이 있는 관계와 성장"],
        study_tips=["🧾 저널링(기록)로 강점/가치 정리", "🗣️ 코칭·상담 스킬 실습", "🎯 ‘내가 바꾸고 싶은 문제’로 프로젝트 설정"],
        keywords=["의미", "상담", "가치", "통찰", "교육"]
    ),
    "INFP": CareerPack(
        tagline="🎨 감성 + 상상력! ‘나다운 길’ 찾기 장인 🌿🫧",
        strengths=["🎭 창의적 표현", "🫶 공감", "🧠 깊은 내적 동기", "🌈 가치 지향"],
        careers=["🎬 콘텐츠 기획/작가", "🎨 디자이너/일러스트", "🧑‍🏫 교육/코칭", "🎧 음악/예술 분야", "🧭 사회적 기업/NGO"],
        environments=["🌿 자율성 + 의미 있는 프로젝트", "🎨 창작을 존중하는 문화", "🧘 압박보다 성장 중심"],
        study_tips=["🧩 포트폴리오(작품) 축적이 최우선", "🧭 가치-직무 매칭 리스트 만들기", "📅 작은 루틴으로 꾸준함 확보"],
        keywords=["창작", "감성", "가치", "표현", "자율"]
    ),
    "ENFJ": CareerPack(
        tagline="🌟 사람을 빛나게 하는 리더! 커뮤니케이션 최강 🫂🎤",
        strengths=["🗣️ 소통·설득", "🤝 팀 빌딩", "🧭 코칭·리딩", "💞 공감"],
        careers=["🧑‍🏫 교사/강사", "🧑‍💼 HR/조직개발", "🎤 MC/커뮤니케이터", "🏥 의료/헬스코치", "📣 PR/브랜드 매니저"],
        environments=["🧑‍🤝‍🧑 협업과 피드백이 활발", "🌱 성장·교육 문화", "🎯 명확한 목표 + 사람 중심"],
        study_tips=["🎤 발표/퍼실리테이션 훈련", "🧾 멘토링/봉사로 경험 쌓기", "📚 심리·교육·리더십 도서 루틴"],
        keywords=["소통", "리더십", "코칭", "교육", "협업"]
    ),
    "ENFP": CareerPack(
        tagline="🔥 에너지 폭발! 사람과 아이디어를 연결하는 네트워커 🌈✨",
        strengths=["💡 아이디어", "🤝 관계 형성", "🎯 동기부여", "🌪️ 변화 적응"],
        careers=["📣 마케터", "🎤 크리에이터/MC", "🧩 서비스 기획", "🧑‍🏫 교육/코치", "🌍 커뮤니티 매니저"],
        environments=["🎉 다양성과 자유를 존중", "🧩 다이나믹한 프로젝트", "🫂 사람과 많이 만나는 역할"],
        study_tips=["📌 관심사→직무 스킬로 번역하기", "🧾 프로젝트/대외활동으로 증명", "📅 ‘재미’와 ‘마감’을 동시에 설계"],
        keywords=["아이디어", "사람", "커뮤니티", "기획", "창의"]
    ),
    "ISTJ": CareerPack(
        tagline="🧱 믿음직한 시스템 메이커! 정확·신뢰의 상징 ✅📌",
        strengths=["📏 꼼꼼함", "🧾 규정·프로세스 준수", "🕰️ 꾸준함", "🛡️ 책임감"],
        careers=["📑 회계/세무", "🏦 금융/리스크관리", "🗂️ 행정/공공기관", "🧪 QC/품질관리", "🛠️ 운영/PMO"],
        environments=["📚 규칙과 역할이 명확", "🧩 안정적인 조직", "📈 장기적으로 숙련이 쌓이는 직무"],
        study_tips=["🧾 체크리스트 기반 학습", "📅 루틴과 반복으로 자동화", "📊 자격증/실무형 포트폴리오"],
        keywords=["규칙", "안정", "정확", "책임", "운영"]
    ),
    "ISFJ": CareerPack(
        tagline="🧸 배려의 전문가! 사람을 편안하게 하는 보호자 🫶🏥",
        strengths=["💞 배려·지원", "📌 실무 감각", "🧩 협업", "🧾 성실함"],
        careers=["🏥 간호/보건", "🧑‍🏫 교육/돌봄", "🧑‍💼 인사/총무", "📚 사서/기록관리", "🧑‍🍳 푸드/서비스 매니저"],
        environments=["🫂 따뜻한 팀 문화", "📌 반복 업무 + 의미", "🧩 안정적 협업 구조"],
        study_tips=["🧾 실습/현장경험을 최우선", "🤝 멘토와 함께 성장 플랜", "📅 꾸준한 루틴으로 역량 축적"],
        keywords=["돌봄", "지원", "안정", "협업", "성실"]
    ),
    "ESTJ": CareerPack(
        tagline="📣 조직의 엔진! 표준화·관리·실행의 달인 🏁🧱",
        strengths=["🗂️ 조직화", "📊 관리·통제", "🚀 실행력", "🧭 리더십"],
        careers=["🏢 운영/관리자", "🧑‍💼 프로젝트 매니저", "🏛️ 공무원/행정", "🧾 재무/기획", "🛒 리테일 매니저"],
        environments=["📌 규칙·역할 명확", "🎯 목표 중심", "🧑‍🤝‍🧑 팀 운영 권한이 있는 자리"],
        study_tips=["📈 KPI로 성과를 보이기", "🧾 표준 프로세스 문서화 훈련", "🗣️ 리더십/코칭 스킬 병행"],
        keywords=["관리", "실행", "조직", "표준", "성과"]
    ),
    "ESFJ": CareerPack(
        tagline="🎀 분위기 메이커! 사람 중심 서비스·조정의 고수 🫂🌟",
        strengths=["🤝 조율", "🗣️ 소통", "💞 공감", "🧑‍🤝‍🧑 팀워크"],
        careers=["🧑‍💼 HR/채용", "🏨 서비스/호텔", "🏥 코디네이터", "📣 PR/홍보", "🧑‍🏫 교육/운영"],
        environments=["🫂 사람과 상호작용이 많은 곳", "🎉 팀 기반 업무", "📌 피드백 문화"],
        study_tips=["🗣️ 대인 커뮤니케이션 훈련", "🧾 CS/운영 매뉴얼 익히기", "📚 심리/리더십 기초 공부"],
        keywords=["서비스", "관계", "조율", "소통", "팀워크"]
    ),
    "ISTP": CareerPack(
        tagline="🛠️ 고장 나면 고치고, 안 되면 새로 만들자! 현실 해결사 ⚙️😎",
        strengths=["🔧 실전 문제 해결", "🧠 침착함", "🛠️ 손기술/도구 활용", "🎯 효율"],
        careers=["🧰 엔지니어/정비", "🧑‍💻 개발자(실무형)", "🕵️ 포렌식/보안", "🎮 게임/테크 아트", "🏥 응급/임상 기술직"],
        environments=["🧪 실험·현장 중심", "🧩 자율적인 문제 해결", "⚡ 빠른 피드백 루프"],
        study_tips=["🛠️ 프로젝트/실습으로 배우기", "🎯 ‘기능 단위’로 쪼개서 완성", "📹 만들면서 기록(튜토리얼/블로그)"],
        keywords=["실전", "기술", "효율", "도구", "문제해결"]
    ),
    "ISFP": CareerPack(
        tagline="🌸 감각적인 크리에이터! 지금-여기에서 빛나는 타입 🎨🫧",
        strengths=["🎨 미적 감각", "🫶 섬세한 공감", "🌿 유연함", "🧩 조용한 몰입"],
        careers=["🎨 디자이너", "📷 사진/영상", "🧑‍🍳 푸드/공예", "🧑‍⚕️ 치료/재활(현장형)", "🪴 라이프스타일 브랜드"],
        environments=["🌿 감각을 살릴 수 있는 곳", "🧘 과도한 경쟁보다 안정", "🎨 창작 존중 문화"],
        study_tips=["🧺 작품/결과물 중심 포트폴리오", "📌 작은 루틴으로 꾸준히", "🤝 협업 시 역할 명확히 하기"],
        keywords=["감각", "창작", "몰입", "유연", "현장"]
    ),
    "ESTP": CareerPack(
        tagline="🏎️ 스피드 & 액션! 현장에서 승부 보는 타입 ⚡🔥",
        strengths=["⚡ 즉흥 대응", "🗣️ 설득", "🎯 실행", "🌪️ 위기 대처"],
        careers=["💼 영업/세일즈", "📣 이벤트/프로모션", "🚓 경찰/소방/현장직", "🎬 방송/리포터", "🏋️ 스포츠/트레이너"],
        environments=["🏁 변화가 많은 현장", "🎯 성과형 보상", "🧑‍🤝‍🧑 사람과 에너지가 많은 곳"],
        study_tips=["🎯 실전 과제/현장 경험 쌓기", "🗣️ 피칭·협상 연습", "📅 짧은 스프린트로 학습"],
        keywords=["액션", "현장", "도전", "성과", "설득"]
    ),
    "ESFP": CareerPack(
        tagline="🎉 무대 체질! 즐거움과 에너지를 전달하는 타입 🌈🎤",
        strengths=["🫂 친화력", "🎭 표현력", "⚡ 즉흥성", "💞 공감"],
        careers=["🎤 MC/방송", "🎬 배우/퍼포머", "📣 마케팅/홍보", "🏨 서비스/관광", "🧑‍🏫 체험형 교육/강사"],
        environments=["🎉 사람 많은 곳", "🌈 자유로운 분위기", "🧩 다양한 업무가 섞인 역할"],
        study_tips=["🎬 무대/프로젝트로 경험 축적", "📱 SNS/포트폴리오 브랜딩", "🧾 피드백을 빠르게 반영"],
        keywords=["표현", "사람", "에너지", "무대", "서비스"]
    ),
}

MBTI_LIST = list(MBTI_DATA.keys())

# -----------------------------
# 🔮 Helper Functions
# -----------------------------
def pick_recommendations(mbti: str, n: int, include_interests: List[str], focus: str):
    pack = MBTI_DATA[mbti]
    base = pack.careers[:]
    random.shuffle(base)

    # 관심사 태그 기반 "가벼운" 가중치 (규칙 기반)
    interest_map = {
        "🧑‍💻 IT/개발": ["개발", "엔지니어", "보안", "데이터", "AI"],
        "🎨 디자인/콘텐츠": ["디자이너", "작가", "콘텐츠", "사진", "영상", "브랜딩", "크리에이터"],
        "🏥 보건/의료": ["간호", "보건", "의료", "임상", "재활", "헬스"],
        "📣 마케팅/세일즈": ["마케팅", "홍보", "PR", "세일즈", "영업", "브랜드"],
        "🏛️ 공공/정책": ["정책", "공공", "행정", "공무원", "연구원"],
        "💼 경영/기획": ["기획", "컨설턴트", "PM", "운영", "사업개발"],
        "🧑‍🏫 교육/상담": ["교육", "교사", "강사", "상담", "코칭", "HR"],
        "⚙️ 기술/현장": ["정비", "현장", "기술", "포렌식", "소방", "경찰"],
    }

    # focus에 따른 키워드
    focus_map = {
        "🎯 안정/전문성": ["관리", "행정", "품질", "회계", "보건", "정책"],
        "🚀 성장/도전": ["창업", "기획", "마케팅", "세일즈", "PM", "컨설턴트"],
        "🎨 창의/표현": ["콘텐츠", "디자이너", "작가", "크리에이터", "브랜딩", "방송"],
        "🧠 연구/분석": ["데이터", "연구원", "AI", "리서처", "퀀트", "정책"],
    }
    focus_kw = focus_map.get(focus, [])

    # 스코어링
    scored = []
    for job in base:
        score = 0
        for it in include_interests:
            for kw in interest_map.get(it, []):
                if kw in job:
                    score += 2
        for kw in focus_kw:
            if kw in job:
                score += 1
        scored.append((score, job))
    scored.sort(key=lambda x: (-x[0], x[1]))
    top = [j for _, j in scored[:n]]

    # 부족하면 채우기
    if len(top) < n:
        for j in base:
            if j not in top:
                top.append(j)
            if len(top) == n:
                break
    return top[:n]

def chips(items: List[str]) -> str:
    return "".join([f"<span class='badge'>{x}</span>" for x in items])

# -----------------------------
# 🧭 UI
# -----------------------------
st.markdown(
    """
<div class="glass">
  <div class="glow-title">✨ MBTI 진로 추천 랩 🚀</div>
  <div class="subtitle">🧭 MBTI를 선택하면, 어울리는 직업과 학습/진로 탐색 팁을 화려하게 추천해드려요. (교육용 가이드)</div>
  <div class="hr"></div>
  <div class="subtitle">📌 참고: MBTI는 ‘결정’이 아니라 ‘탐색’을 돕는 도구예요. 흥미·가치·역량·경험을 함께 보세요.</div>
</div>
""",
    unsafe_allow_html=True
)

left, right = st.columns([0.42, 0.58], gap="large")

with left:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.subheader("🧩 내 MBTI 선택하기")
    mbti = st.selectbox("🔮 MBTI를 골라주세요", MBTI_LIST, index=0)

    st.markdown("#### 🌟 관심 분야(선택)로 추천을 더 맞춰볼까요?")
    interests = st.multiselect(
        "좋아하는 분야를 체크하면 추천 직업이 조금 더 정교해져요 🎯",
        ["🧑‍💻 IT/개발", "🎨 디자인/콘텐츠", "🏥 보건/의료", "📣 마케팅/세일즈",
         "🏛️ 공공/정책", "💼 경영/기획", "🧑‍🏫 교육/상담", "⚙️ 기술/현장"],
        default=[]
    )

    focus = st.selectbox(
        "💎 이번 탐색의 ‘우선순위’를 골라주세요",
        ["🎯 안정/전문성", "🚀 성장/도전", "🎨 창의/표현", "🧠 연구/분석"],
        index=1
    )

    count = st.slider("🎁 추천 직업 개수", min_value=3, max_value=10, value=6, step=1)

    go = st.button("🚀 추천 결과 보기!")
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    pack = MBTI_DATA[mbti]

    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.subheader(f"🔍 {mbti} 분석 리포트 🧾✨")
    st.markdown(f"### {pack.tagline}")

    st.markdown("#### 💪 강점 키워드")
    st.markdown(chips(pack.strengths), unsafe_allow_html=True)

    st.markdown("#### 🧠 적성/흥미 키워드")
    st.markdown(chips([f"🌈 {k}" for k in pack.keywords]), unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.subheader("🧰 추천 직업 리스트 (맞춤형) 💼✨")

    if go:
        recs = pick_recommendations(mbti, count, interests, focus)
    else:
        recs = pack.careers[:min(6, len(pack.careers))]

    for i, job in enumerate(recs, start=1):
        st.markdown(
            f"""
<div class="glass" style="padding:14px; margin-bottom:12px;">
  <div style="display:flex; align-items:center; justify-content:space-between;">
    <div style="font-size:18px; font-weight:900;">{i}. {job} 💎</div>
    <div style="opacity:0.9;">🧠 {mbti} → 🎯 {focus}</div>
  </div>
  <div class="hr"></div>
  <div style="font-size:14px; opacity:0.92;">
    ✅ 추천 포인트: <b>{random.choice(pack.strengths)}</b> 를(을) 활용하기 좋아요.<br/>
    🧩 잘 맞는 환경: <b>{random.choice(pack.environments)}</b><br/>
    📚 성장 팁: <b>{random.choice(pack.study_tips)}</b>
  </div>
</div>
""",
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    with st.expander("🧪 (확장) 추천이 더 정확해지려면? 🔍✨"):
        st.markdown(
            """
- 🧭 **흥미(What I like)**: 어떤 과제/활동에서 시간이 빨리 가나요?  
- 🧠 **역량(What I can do)**: 내가 잘하는 스킬(논리/소통/창작/정리/현장 등)은 무엇인가요?  
- 💎 **가치(What matters)**: 돈/안정/성장/의미/자율/명예 중 무엇이 중요한가요?  
- 🧪 **경험(What I tried)**: 작은 프로젝트/동아리/인턴/대외활동으로 “해봤다”를 늘리면 진로가 빨리 선명해져요.  
            """
        )

# Footer
st.markdown(
    """
<div style="margin-top:16px; text-align:center; opacity:0.85;">
  <div class="glass">
    🧭 Made with Streamlit ✨ | 🎓 진로 교육용 가이드 | 🚀 당신의 가능성은 MBTI보다 훨씬 넓어요 🌌
  </div>
</div>
""",
    unsafe_allow_html=True
)
