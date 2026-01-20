import streamlit as st
from dataclasses import dataclass
from typing import List, Dict
import random

st.set_page_config(
    page_title="MBTI 진로 추천",
    page_icon="🧭",
    layout="wide",
)

# -----------------------------
# 🎨 Minimal White/Blue UI
# -----------------------------
CUSTOM_CSS = """
<style>
/* 전체 배경: 화이트 */
.stApp {
  background: #F7FAFF;
  color: #0B1B3A;
}

/* 공통 폰트 */
html, body, [class*="css"]  {
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, "Noto Sans KR", "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
}

/* 상단 헤더 */
.header {
  background: linear-gradient(90deg, #0B63F6 0%, #2EA8FF 100%);
  padding: 18px 20px;
  border-radius: 14px;
  color: white;
  box-shadow: 0 10px 26px rgba(11,99,246,0.18);
}
.header h1{
  margin:0;
  font-size: 28px;
  font-weight: 900;
  letter-spacing: -0.3px;
}
.header p{
  margin:6px 0 0 0;
  font-size: 14px;
  opacity: 0.92;
}

/* 카드 (심플) */
.card {
  background: #FFFFFF;
  border: 1px solid rgba(11, 99, 246, 0.12);
  border-radius: 14px;
  padding: 16px 16px 12px 16px;
  box-shadow: 0 8px 22px rgba(17, 34, 68, 0.06);
}
.card + .card { margin-top: 12px; }

/* 섹션 타이틀 */
.section-title{
  font-size: 16px;
  font-weight: 900;
  color: #083A99;
  margin: 0 0 10px 0;
}

/* 뱃지 */
.badge {
  display:inline-block;
  padding: 6px 10px;
  border-radius: 999px;
  background: rgba(11, 99, 246, 0.08);
  border: 1px solid rgba(11, 99, 246, 0.14);
  color: #063A8C;
  margin-right: 6px;
  margin-bottom: 6px;
  font-size: 13px;
  font-weight: 700;
}

/* 버튼 */
div.stButton > button {
  background: #0B63F6;
  color: white;
  font-weight: 900;
  border: 1px solid rgba(11, 99, 246, 0.35);
  border-radius: 12px;
  padding: 0.75rem 1.1rem;
  box-shadow: 0 10px 22px rgba(11,99,246,0.18);
}
div.stButton > button:hover {
  background: #0957D8;
}

/* selectbox, multiselect */
[data-baseweb="select"] > div {
  background: #FFFFFF !important;
  border-radius: 12px !important;
  border: 1px solid rgba(11, 99, 246, 0.18) !important;
}

/* 작은 안내문 */
.note {
  color: rgba(11, 27, 58, 0.72);
  font-size: 13px;
  line-height: 1.5;
}

/* 구분선 */
.hr {
  height: 1px;
  background: rgba(11, 99, 246, 0.12);
  margin: 12px 0;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -----------------------------
# 🧩 Data Model
# -----------------------------
@dataclass
class CareerPack:
    summary: str                 # 간결 리포트
    strengths: List[str]
    careers: List[str]
    environments: List[str]
    study_tips: List[str]
    famous_people: List[str]     # MBTI별 유명인 (예시)
    keywords: List[str]

def chips(items: List[str]) -> str:
    return "".join([f"<span class='badge'>{x}</span>" for x in items])

# -----------------------------
# 🧠 MBTI Data (간결 버전 + 유명인 추가)
# ※ 유명인 MBTI는 출처/기준에 따라 논쟁이 있을 수 있어 "대표적으로 언급되는 예시"로 제시
# -----------------------------
MBTI_DATA: Dict[str, CareerPack] = {
    "INTJ": CareerPack(
        summary="전략·분석 중심. 복잡한 문제를 구조화하고 장기 로드맵을 설계하는 데 강함.",
        strengths=["전략", "분석", "최적화", "독립적 사고"],
        careers=["데이터 사이언티스트", "전략 컨설턴트", "제품 매니저(PM)", "정책/기획 연구원", "보안 분석가"],
        environments=["자율성 높은 조직", "깊이 있는 프로젝트", "목표·지표가 명확한 팀"],
        study_tips=["로드맵 먼저", "핵심개념→응용", "성과(포트폴리오)로 증명"],
        famous_people=["Elon Musk", "Christopher Nolan", "Michelle Obama"],
        keywords=["전략", "기획", "분석"]
    ),
    "INTP": CareerPack(
        summary="원리 탐구형. 개념을 연결하고 가설을 세워 실험하며 답을 찾아가는 스타일.",
        strengths=["논리", "탐구", "모델링", "문제 해결"],
        careers=["소프트웨어 엔지니어", "R&D 연구원", "AI/알고리즘 엔지니어", "UX 리서처", "퀀트/리서치"],
        environments=["실험과 탐색이 허용", "지적 호기심을 존중", "프로젝트 기반"],
        study_tips=["작게 만들어 검증", "완벽주의 대신 v1", "스터디로 마감 확보"],
        famous_people=["Albert Einstein", "Bill Gates", "Marie Curie"],
        keywords=["탐구", "이론", "실험"]
    ),
    "ENTJ": CareerPack(
        summary="목표 달성형 리더. 의사결정이 빠르고 실행·조직 운영에 강점.",
        strengths=["리더십", "결정", "추진", "성과 관리"],
        careers=["사업개발(BD)", "경영 컨설턴트", "프로덕트 오너", "운영/조직 관리자", "세일즈 리더"],
        environments=["성과 중심", "역할이 명확", "속도감 있는 조직"],
        study_tips=["KPI 기반 사례 만들기", "발표·협상 훈련", "케이스 스터디"],
        famous_people=["Steve Jobs", "Margaret Thatcher", "Gordon Ramsay"],
        keywords=["리더십", "성과", "비즈니스"]
    ),
    "ENTP": CareerPack(
        summary="아이디어·설득형. 변화와 혁신을 즐기며 토론·기획에 강함.",
        strengths=["발상", "토론", "설득", "적응"],
        careers=["창업", "마케팅/브랜딩", "기획자", "정책/커뮤니케이션", "미디어/콘텐츠"],
        environments=["자유로운 아이디어 문화", "빠른 실험", "다양한 협업"],
        study_tips=["프로젝트로 학습", "피칭 경험", "마감 관리"],
        famous_people=["Thomas Edison", "Mark Twain", "Sacha Baron Cohen"],
        keywords=["혁신", "기획", "설득"]
    ),
    "INFJ": CareerPack(
        summary="의미·사람 중심. 통찰과 공감을 바탕으로 장기 성장과 변화를 돕는 타입.",
        strengths=["통찰", "공감", "가치 지향", "기획력"],
        careers=["상담/심리", "교육", "HR/조직문화", "에디터/작가", "사회혁신/NGO"],
        environments=["미션 중심", "깊이 있는 관계", "조용히 몰입 가능한 환경"],
        study_tips=["기록(저널링)", "코칭/상담 실습", "문제 중심 프로젝트"],
        famous_people=["Martin Luther King Jr.", "Nelson Mandela", "Mother Teresa"],
        keywords=["의미", "상담", "교육"]
    ),
    "INFP": CareerPack(
        summary="가치·창의 중심. ‘나다움’을 살리는 표현/콘텐츠/브랜딩에서 강점.",
        strengths=["창의", "공감", "가치", "스토리텔링"],
        careers=["콘텐츠 기획/작가", "디자이너", "교육/코칭", "예술 분야", "사회적 기업/NGO"],
        environments=["자율성 높은 문화", "창작 존중", "성장 중심"],
        study_tips=["결과물(작품) 축적", "가치-직무 매칭", "작은 루틴 유지"],
        famous_people=["William Shakespeare", "J.R.R. Tolkien", "Audrey Hepburn"],
        keywords=["창작", "가치", "표현"]
    ),
    "ENFJ": CareerPack(
        summary="사람을 성장시키는 리더형. 코칭·조직 운영·커뮤니케이션에 강함.",
        strengths=["소통", "코칭", "팀 빌딩", "리딩"],
        careers=["교사/강사", "HR/조직개발", "PR/브랜드", "헬스코치", "커뮤니케이터"],
        environments=["협업이 활발", "피드백 문화", "성장·교육 친화"],
        study_tips=["퍼실리테이션", "멘토링 경험", "심리/리더십 기초"],
        famous_people=["Barack Obama", "Oprah Winfrey", "Emma Watson"],
        keywords=["소통", "코칭", "리더십"]
    ),
    "ENFP": CareerPack(
        summary="아이디어·관계형. 사람과 기회를 연결하며 다양한 프로젝트에서 빛남.",
        strengths=["아이디어", "관계", "동기부여", "적응"],
        careers=["마케터", "서비스/콘텐츠 기획", "교육/코치", "커뮤니티 매니저", "크리에이터"],
        environments=["다양성 존중", "프로젝트가 다채로움", "사람 중심 역할"],
        study_tips=["흥미→스킬로 번역", "대외활동/프로젝트", "재미+마감 설계"],
        famous_people=["Robin Williams", "Walt Disney", "Will Smith"],
        keywords=["사람", "기획", "창의"]
    ),
    "ISTJ": CareerPack(
        summary="신뢰·정확 중심. 규정과 프로세스를 기반으로 안정적으로 성과를 만든다.",
        strengths=["꼼꼼", "책임", "프로세스", "꾸준함"],
        careers=["회계/세무", "리스크관리", "행정/공공", "품질관리(QC)", "PMO/운영"],
        environments=["규칙과 역할이 명확", "안정적 조직", "숙련이 쌓이는 직무"],
        study_tips=["체크리스트", "루틴 반복", "자격/실무 포트폴리오"],
        famous_people=["George Washington", "Angela Merkel", "Natalie Portman"],
        keywords=["정확", "안정", "운영"]
    ),
    "ISFJ": CareerPack(
        summary="배려·지원 중심. 실무 감각이 좋고 돌봄/지원 역할에서 강함.",
        strengths=["배려", "성실", "협업", "실무"],
        careers=["보건/간호", "교육/돌봄", "인사/총무", "기록관리", "서비스 운영"],
        environments=["따뜻한 팀 문화", "안정적 협업", "의미 있는 반복 업무"],
        study_tips=["현장 실습", "멘토 기반 성장", "꾸준한 루틴"],
        famous_people=["Beyoncé", "Queen Elizabeth II", "Vin Diesel"],
        keywords=["돌봄", "지원", "성실"]
    ),
    "ESTJ": CareerPack(
        summary="관리·실행 중심. 표준화와 운영을 통해 조직의 성과를 끌어올린다.",
        strengths=["조직화", "실행", "관리", "리더십"],
        careers=["운영/관리자", "프로젝트 매니저", "행정", "재무/기획", "리테일 매니저"],
        environments=["목표 중심", "역할 명확", "운영 권한이 있는 자리"],
        study_tips=["성과 사례 만들기", "프로세스 문서화", "코칭 스킬 병행"],
        famous_people=["Henry Ford", "John D. Rockefeller", "Judge Judy"],
        keywords=["관리", "실행", "조직"]
    ),
    "ESFJ": CareerPack(
        summary="관계·조율 중심. 팀워크와 커뮤니케이션으로 분위기와 성과를 함께 만든다.",
        strengths=["소통", "조율", "팀워크", "서비스 마인드"],
        careers=["HR/채용", "서비스/관광", "코디네이터", "홍보/PR", "교육 운영"],
        environments=["상호작용이 많은 곳", "팀 기반", "피드백 문화"],
        study_tips=["대인 커뮤니케이션", "운영 매뉴얼", "심리/리더십 기초"],
        famous_people=["Taylor Swift", "Jennifer Lopez", "Bill Clinton"],
        keywords=["관계", "서비스", "조율"]
    ),
    "ISTP": CareerPack(
        summary="현실 해결형. 실전에서 빠르게 원인을 찾고 효율적으로 고친다.",
        strengths=["실전", "침착", "효율", "도구 활용"],
        careers=["엔지니어/정비", "실무형 개발", "보안/포렌식", "테크 아트", "임상 기술직"],
        environments=["현장 중심", "자율 문제 해결", "빠른 피드백"],
        study_tips=["실습/프로젝트", "기능 단위 완성", "기록으로 축적"],
        famous_people=["Clint Eastwood", "Bear Grylls", "Scarlett Johansson"],
        keywords=["실전", "기술", "효율"]
    ),
    "ISFP": CareerPack(
        summary="감각·몰입형. 미적 감각과 섬세함을 살려 ‘좋은 결과물’을 만든다.",
        strengths=["감각", "섬세", "유연", "몰입"],
        careers=["디자이너", "사진/영상", "공예/푸드", "치료/재활(현장형)", "라이프스타일 브랜드"],
        environments=["감각을 살릴 수 있는 곳", "안정적 몰입", "창작 존중"],
        study_tips=["포트폴리오 중심", "작은 루틴", "역할 명확한 협업"],
        famous_people=["Michael Jackson", "Frida Kahlo", "David Beckham"],
        keywords=["감각", "창작", "몰입"]
    ),
    "ESTP": CareerPack(
        summary="스피드·현장형. 즉시 실행과 설득, 위기 대처에서 강점.",
        strengths=["액션", "설득", "대응", "실행"],
        careers=["영업/세일즈", "이벤트/프로모션", "현장직(경찰/소방)", "리포터", "트레이너"],
        environments=["변화 많은 현장", "성과형 보상", "에너지 높은 조직"],
        study_tips=["현장 경험", "피칭/협상", "짧은 스프린트 학습"],
        famous_people=["Donald Trump", "Madonna", "Eddie Murphy"],
        keywords=["현장", "도전", "성과"]
    ),
    "ESFP": CareerPack(
        summary="표현·관계형. 분위기와 에너지를 살려 사람 중심 역할에서 두각.",
        strengths=["표현", "친화", "공감", "즉흥"],
        careers=["MC/방송", "퍼포머", "마케팅/홍보", "관광/서비스", "체험형 교육/강사"],
        environments=["사람 많은 곳", "자유로운 분위기", "다양한 업무"],
        study_tips=["무대/프로젝트 경험", "개인 브랜딩", "빠른 피드백 반영"],
        famous_people=["Marilyn Monroe", "Elton John", "Jamie Oliver"],
        keywords=["표현", "사람", "에너지"]
    ),
}

MBTI_LIST = list(MBTI_DATA.keys())

# -----------------------------
# 🔧 Recommendation helper
# -----------------------------
def pick_recommendations(mbti: str, n: int, include_interests: List[str]) -> List[str]:
    pack = MBTI_DATA[mbti]
    base = pack.careers[:]

    # 관심사 기반 간단 가중치 (심플 유지)
    interest_map = {
        "IT/개발": ["개발", "엔지니어", "보안", "데이터", "AI"],
        "디자인/콘텐츠": ["디자이너", "작가", "콘텐츠", "사진", "영상", "브랜딩", "크리에이터", "미디어"],
        "보건/의료": ["보건", "간호", "의료", "임상", "재활", "헬스"],
        "마케팅/세일즈": ["마케팅", "홍보", "PR", "세일즈", "영업", "브랜드", "프로모션"],
        "공공/정책": ["정책", "공공", "행정", "연구원"],
        "경영/기획": ["기획", "컨설턴트", "PM", "운영", "사업개발", "프로젝트"],
        "교육/상담": ["교육", "교사", "강사", "상담", "코칭", "HR"],
        "기술/현장": ["정비", "현장", "기술", "포렌식", "소방", "경찰"],
    }

    scored = []
    for job in base:
        score = 0
        for it in include_interests:
            for kw in interest_map.get(it, []):
                if kw in job:
                    score += 2
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

# -----------------------------
# 🧭 Header
# -----------------------------
st.markdown(
    """
<div class="header">
  <h1>MBTI 진로 추천 🧭</h1>
</div>
""",
    unsafe_allow_html=True
)

st.write("")  # spacing

left, right = st.columns([0.36, 0.64], gap="large")

with left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>선택</div>", unsafe_allow_html=True)

    mbti = st.selectbox("MBTI", MBTI_LIST, index=0)

    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    st.markdown("<div class='note'>관심 분야(선택)를 체크하면 추천 직업이 조금 더 정교해집니다.</div>", unsafe_allow_html=True)

    interests = st.multiselect(
        "관심 분야",
        ["IT/개발", "디자인/콘텐츠", "보건/의료", "마케팅/세일즈", "공공/정책", "경영/기획", "교육/상담", "기술/현장"],
        default=[]
    )

    count = st.slider("추천 직업 개수", min_value=3, max_value=10, value=6, step=1)

    go = st.button("추천 보기")
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    pack = MBTI_DATA[mbti]

    # 간결 리포트
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>간단 리포트</div>", unsafe_allow_html=True)
    st.write(f"**{mbti}** — {pack.summary}")

    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    st.markdown("**핵심 강점**", help="MBTI는 참고 지표이며, 실제 진로는 흥미·역량·경험을 함께 고려하세요.")
    st.markdown(chips([f"🔹 {s}" for s in pack.strengths]), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 추천 직업
    recs = pick_recommendations(mbti, count, interests) if go else pack.careers[:min(6, len(pack.careers))]

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>추천 직업</div>", unsafe_allow_html=True)

    for i, job in enumerate(recs, start=1):
        env = random.choice(pack.environments)
        tip = random.choice(pack.study_tips)
        st.markdown(
            f"""
<div style="padding:10px 12px; border: 1px solid rgba(11,99,246,0.12); border-radius: 12px; background: rgba(11,99,246,0.03); margin-bottom:10px;">
  <div style="font-weight:900; color:#083A99;">{i}. {job}</div>
  <div style="font-size:13px; color: rgba(11,27,58,0.82); margin-top:4px;">
    • 환경: {env}<br/>
    • 팁: {tip}
  </div>
</div>
""",
            unsafe_allow_html=True
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # 유명인
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>대표적으로 언급되는 유명인</div>", unsafe_allow_html=True)
    st.markdown(chips([f"⭐ {p}" for p in pack.famous_people]), unsafe_allow_html=True)
    st.markdown(
        "<div class='note'>참고: 유명인 MBTI는 출처에 따라 달라질 수 있어, ‘대표적으로 언급되는 예시’로 제공됩니다.</div>",
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.write("")
st.markdown(
    "<div class='note' style='text-align:center;'>© MBTI Career Guide — Simple White & Blue UI</div>",
    unsafe_allow_html=True
)
