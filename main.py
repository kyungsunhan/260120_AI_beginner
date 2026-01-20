import streamlit as st
from dataclasses import dataclass
from typing import List, Dict, Optional
import textwrap

# =============================
# ✅ Page config
# =============================
st.set_page_config(
    page_title="🌈 어깨 통증 검사 & 운동 가이드",
    page_icon="🦴",
    layout="wide",
)

# =============================
# 🎨 White background + flashy accents + lots of emoji
# =============================
CSS = """
<style>
/* --- 전체: 화이트 배경 --- */
.stApp{
  background: #ffffff;
  color: #101828;
}

/* --- 폰트 --- */
html, body, [class*="css"]{
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, "Noto Sans KR",
               "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
}

/* --- 상단 히어로(그라데이션) --- */
.hero{
  border-radius: 18px;
  padding: 18px 20px;
  background:
    radial-gradient(circle at 10% 20%, rgba(255, 88, 174, 0.20), transparent 40%),
    radial-gradient(circle at 90% 20%, rgba(0, 209, 255, 0.18), transparent 40%),
    radial-gradient(circle at 30% 90%, rgba(0, 255, 187, 0.14), transparent 45%),
    linear-gradient(90deg, #0B63F6 0%, #2EA8FF 45%, #7C3AED 100%);
  box-shadow: 0 16px 40px rgba(12, 74, 255, 0.18);
  color: white;
}
.hero-title{
  margin: 0;
  font-size: 28px;
  font-weight: 900;
  letter-spacing: -0.4px;
  text-shadow: 0 10px 30px rgba(0,0,0,0.25);
}
.hero-sub{
  margin-top: 6px;
  font-size: 13.5px;
  opacity: 0.95;
  line-height: 1.45;
}

/* --- 카드: 스티커/글라스 느낌 --- */
.card{
  background: rgba(255,255,255,0.92);
  border: 1px solid rgba(15, 23, 42, 0.10);
  border-radius: 18px;
  padding: 16px 16px 12px 16px;
  box-shadow: 0 14px 40px rgba(2, 6, 23, 0.08);
}
.card + .card{ margin-top: 14px; }

.section-title{
  font-size: 15px;
  font-weight: 900;
  margin: 0 0 10px 0;
  letter-spacing: -0.2px;
}

/* --- 섹션 라벨(그라데이션 텍스트) --- */
.grad-text{
  background: linear-gradient(90deg, #0B63F6, #2EA8FF, #7C3AED, #FF58AE);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* --- 배지(칩) --- */
.badge{
  display:inline-block;
  padding: 6px 10px;
  border-radius: 999px;
  background: rgba(11, 99, 246, 0.08);
  border: 1px solid rgba(11, 99, 246, 0.14);
  color: #0B63F6;
  margin-right: 6px;
  margin-bottom: 6px;
  font-size: 13px;
  font-weight: 800;
}

/* --- 구분선(컨페티 라인) --- */
.hr{
  height: 1px;
  margin: 12px 0;
  background: linear-gradient(90deg, transparent, rgba(11,99,246,0.25), rgba(255,88,174,0.25), transparent);
}

/* --- 안내문 --- */
.note{
  color: rgba(16, 24, 40, 0.72);
  font-size: 13px;
  line-height: 1.55;
}
.small{
  color: rgba(16, 24, 40, 0.68);
  font-size: 12.5px;
  line-height: 1.5;
}

/* --- 버튼: 캔디 그라데이션 --- */
div.stButton > button{
  background: linear-gradient(90deg, #0B63F6 0%, #2EA8FF 40%, #7C3AED 80%, #FF58AE 100%);
  color: white;
  font-weight: 900;
  border: none;
  border-radius: 14px;
  padding: 0.78rem 1.0rem;
  box-shadow: 0 16px 36px rgba(11,99,246,0.22);
}
div.stButton > button:hover{
  filter: brightness(1.03);
  transform: translateY(-1px);
}

/* --- 셀렉트 박스 --- */
[data-baseweb="select"] > div{
  background: #ffffff !important;
  border-radius: 14px !important;
  border: 1px solid rgba(11, 99, 246, 0.18) !important;
  box-shadow: 0 10px 22px rgba(2, 6, 23, 0.05);
}

/* --- expander 타이틀 가독성 --- */
details summary{
  font-weight: 900 !important;
}

/* --- SVG wrapper --- */
.svgwrap{
  border: 1px solid rgba(11, 99, 246, 0.14);
  border-radius: 14px;
  background: linear-gradient(180deg, rgba(11,99,246,0.05), rgba(255,88,174,0.03));
  padding: 10px;
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# =============================
# Models
# =============================
@dataclass
class PhysicalTest:
    name: str
    target: str
    how: str
    positive: str
    caution: Optional[str] = None

@dataclass
class Exercise:
    name: str
    goal: str
    steps: List[str]
    dosage: str
    svg: str
    cautions: Optional[str] = None

def chips(items: List[str]) -> str:
    return "".join([f"<span class='badge'>{x}</span>" for x in items])

def wrap(s: str) -> str:
    return "\n".join(textwrap.wrap(s, width=88))

def svg_card(svg: str) -> str:
    return f"<div class='svgwrap'>{svg}</div>"

# =============================
# SVG diagrams (simple)
# =============================
SVG_PENDULUM = """
<svg width="520" height="180" viewBox="0 0 520 180" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="520" height="180" rx="12" fill="white"/>
  <text x="18" y="26" font-size="14" font-weight="800" fill="#0B63F6">🌀 Pendulum (Codman) - 팔 흔들기</text>
  <rect x="40" y="72" width="190" height="12" rx="6" fill="#2EA8FF" opacity="0.25"/>
  <circle cx="95" cy="62" r="10" fill="#0B63F6" opacity="0.9"/>
  <line x1="95" y1="72" x2="120" y2="110" stroke="#0B63F6" stroke-width="6" stroke-linecap="round"/>
  <line x1="120" y1="110" x2="155" y2="120" stroke="#0B63F6" stroke-width="6" stroke-linecap="round"/>
  <line x1="120" y1="110" x2="80" y2="78" stroke="#0B63F6" stroke-width="5" stroke-linecap="round" opacity="0.85"/>
  <line x1="155" y1="120" x2="175" y2="150" stroke="#0B63F6" stroke-width="6" stroke-linecap="round"/>
  <circle cx="175" cy="150" r="6" fill="#0B63F6" opacity="0.95"/>
  <path d="M175 150 C205 140, 220 125, 230 110" fill="none" stroke="#FF58AE" stroke-width="3" stroke-dasharray="6 6"/>
  <path d="M175 150 C150 140, 135 125, 125 110" fill="none" stroke="#FF58AE" stroke-width="3" stroke-dasharray="6 6"/>
  <text x="255" y="122" font-size="12" fill="#101828" opacity="0.75">✨ 작게 원/좌우로 흔들기</text>
  <text x="300" y="150" font-size="12" fill="#101828" opacity="0.75">✅ 통증 범위 내에서</text>
</svg>
"""

SVG_SCAP_RETRACT = """
<svg width="520" height="180" viewBox="0 0 520 180" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="520" height="180" rx="12" fill="white"/>
  <text x="18" y="26" font-size="14" font-weight="800" fill="#0B63F6">🪽 Scapular Retraction - 견갑골 모으기</text>
  <circle cx="130" cy="60" r="10" fill="#0B63F6" opacity="0.9"/>
  <line x1="130" y1="70" x2="130" y2="130" stroke="#0B63F6" stroke-width="8" stroke-linecap="round"/>
  <line x1="110" y1="92" x2="150" y2="92" stroke="#0B63F6" stroke-width="6" stroke-linecap="round" opacity="0.9"/>
  <path d="M115 108 Q130 95 145 108" fill="none" stroke="#2EA8FF" stroke-width="4"/>
  <path d="M115 118 Q130 105 145 118" fill="none" stroke="#2EA8FF" stroke-width="4"/>
  <line x1="85" y1="112" x2="110" y2="112" stroke="#FF58AE" stroke-width="3"/>
  <polygon points="110,112 103,108 103,116" fill="#FF58AE"/>
  <line x1="175" y1="112" x2="150" y2="112" stroke="#FF58AE" stroke-width="3"/>
  <polygon points="150,112 157,108 157,116" fill="#FF58AE"/>
  <text x="220" y="90" font-size="12" fill="#101828" opacity="0.75">✅ 어깨 으쓱 NO</text>
  <text x="220" y="112" font-size="12" fill="#101828" opacity="0.75">✨ 날개뼈를 뒤로/아래로</text>
</svg>
"""

SVG_ER_BAND = """
<svg width="520" height="180" viewBox="0 0 520 180" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="520" height="180" rx="12" fill="white"/>
  <text x="18" y="26" font-size="14" font-weight="800" fill="#0B63F6">🧲 External Rotation - 외회전 밴드</text>
  <circle cx="120" cy="58" r="10" fill="#0B63F6" opacity="0.9"/>
  <line x1="120" y1="68" x2="120" y2="132" stroke="#0B63F6" stroke-width="8" stroke-linecap="round"/>
  <line x1="120" y1="92" x2="160" y2="92" stroke="#0B63F6" stroke-width="6" stroke-linecap="round"/>
  <line x1="160" y1="92" x2="160" y2="120" stroke="#0B63F6" stroke-width="6" stroke-linecap="round"/>
  <rect x="118" y="98" width="10" height="18" rx="4" fill="#2EA8FF" opacity="0.45"/>
  <text x="185" y="98" font-size="12" fill="#101828" opacity="0.75">🧻 수건 끼우면 좋음</text>
  <circle cx="260" cy="92" r="6" fill="#0B63F6" opacity="0.9"/>
  <line x1="260" y1="92" x2="160" y2="110" stroke="#2EA8FF" stroke-width="4"/>
  <text x="270" y="95" font-size="12" fill="#101828" opacity="0.75">📌 고정점</text>
  <path d="M165 122 A30 30 0 0 0 195 112" fill="none" stroke="#FF58AE" stroke-width="3"/>
  <polygon points="195,112 188,110 190,117" fill="#FF58AE"/>
  <text x="220" y="130" font-size="12" fill="#101828" opacity="0.75">✨ 천천히 바깥으로</text>
</svg>
"""

SVG_DOORWAY = """
<svg width="520" height="180" viewBox="0 0 520 180" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="520" height="180" rx="12" fill="white"/>
  <text x="18" y="26" font-size="14" font-weight="800" fill="#0B63F6">🚪 Doorway Stretch - 흉근 스트레칭</text>
  <rect x="300" y="48" width="22" height="110" fill="#2EA8FF" opacity="0.22"/>
  <rect x="420" y="48" width="22" height="110" fill="#2EA8FF" opacity="0.22"/>
  <rect x="300" y="48" width="142" height="18" fill="#2EA8FF" opacity="0.22"/>
  <circle cx="140" cy="68" r="10" fill="#0B63F6" opacity="0.9"/>
  <line x1="140" y1="78" x2="140" y2="140" stroke="#0B63F6" stroke-width="8" stroke-linecap="round"/>
  <line x1="140" y1="95" x2="190" y2="80" stroke="#0B63F6" stroke-width="6" stroke-linecap="round"/>
  <line x1="140" y1="95" x2="190" y2="110" stroke="#0B63F6" stroke-width="6" stroke-linecap="round"/>
  <line x1="190" y1="80" x2="300" y2="68" stroke="#FF58AE" stroke-width="3" stroke-dasharray="6 6"/>
  <line x1="190" y1="110" x2="300" y2="120" stroke="#FF58AE" stroke-width="3" stroke-dasharray="6 6"/>
  <line x1="165" y1="150" x2="210" y2="150" stroke="#FF58AE" stroke-width="3"/>
  <polygon points="210,150 203,146 203,154" fill="#FF58AE"/>
  <text x="220" y="154" font-size="12" fill="#101828" opacity="0.75">✨ 가슴을 앞으로</text>
</svg>
"""

# =============================
# Data
# =============================
TESTS: Dict[str, PhysicalTest] = {
    "Neer": PhysicalTest(
        name="🧪 Neer Impingement",
        target="견봉하 충돌/회전근개 병변(충돌 기전)",
        how="견갑을 고정한 뒤, 팔을 내회전 상태로 전방거상(끝범위까지).",
        positive="전외측 어깨 통증/불편감 재현(특히 70–120° 또는 끝범위).",
        caution="급성 통증이 매우 심하면 범위를 줄이거나 중단."
    ),
    "Hawkins": PhysicalTest(
        name="🧪 Hawkins-Kennedy",
        target="견봉하 충돌",
        how="어깨 90° 굴곡 + 팔꿈치 90° 굴곡 후, 전완을 내회전.",
        positive="전외측 어깨 통증 재현."
    ),
    "PainfulArc": PhysicalTest(
        name="🧪 Painful Arc",
        target="견봉하 충돌/상완골두-견봉 간 문제",
        how="팔을 외전(옆으로 올리기)하며 통증 구간 확인.",
        positive="대개 60–120° 구간 통증↑ 후 그 이상에서 감소."
    ),
    "EmptyCan": PhysicalTest(
        name="🧪 Empty Can (Jobe)",
        target="극상근(supraspinatus) 관련",
        how="90° 외전+30° 전방(Scaption)에서 엄지 아래로, 저항을 버팀.",
        positive="통증 또는 근력 저하(좌우 비교).",
        caution="통증이 심하면 Full Can(엄지 위)로 대체 고려."
    ),
    "DropArm": PhysicalTest(
        name="🧪 Drop Arm",
        target="전층 회전근개 파열 가능(특히 극상근)",
        how="팔을 외전시킨 뒤 천천히 내리게 함.",
        positive="버티지 못하고 갑자기 떨어짐/조절 불가."
    ),
    "ERLag": PhysicalTest(
        name="🧪 ER Lag Sign",
        target="후방 회전근개(극하근/소원근) 파열 가능",
        how="외회전 최대로 위치 → 유지하도록 함.",
        positive="외회전 유지 못하고 내회전으로 흘러내림."
    ),
    "LiftOff": PhysicalTest(
        name="🧪 Lift-off",
        target="견갑하근(subscapularis)",
        how="손등을 허리 뒤에 두고 등에서 떼어 올림.",
        positive="손을 떼지 못함/약함/통증."
    ),
    "BellyPress": PhysicalTest(
        name="🧪 Belly-press",
        target="견갑하근 대체 검사",
        how="손바닥을 복부에 대고 팔꿈치를 앞으로 유지한 채 누름.",
        positive="팔꿈치가 뒤로 빠짐(보상) 또는 힘/통증 문제."
    ),
    "Speed": PhysicalTest(
        name="🧪 Speed Test",
        target="상완이두근 장두/SLAP 의심",
        how="팔 90° 전방거상, 팔꿈치 신전, 전완 회외 상태에서 저항.",
        positive="이두구(bicipital groove) 통증."
    ),
    "Yergason": PhysicalTest(
        name="🧪 Yergason",
        target="이두근 장두/횡상완인대",
        how="팔꿈치 90° 굴곡, 전완 회외+외회전에 저항.",
        positive="이두구 통증/불안정 느낌."
    ),
    "OBrien": PhysicalTest(
        name="🧪 O’Brien",
        target="SLAP / AC joint",
        how="90° 굴곡+내전, 엄지 아래 저항 → 엄지 위로 반복 비교.",
        positive="내회전에서 통증↑, 외회전에서 감소(패턴 확인)."
    ),
    "CrossBody": PhysicalTest(
        name="🧪 Cross-body Adduction",
        target="AC joint 병변",
        how="팔 90° 굴곡 후 몸통 쪽으로 가로질러 내전.",
        positive="AC joint 부위 국소 통증."
    ),
    "Apprehension": PhysicalTest(
        name="🧪 Apprehension/Relocation",
        target="전방 불안정/재발성 탈구",
        how="외전+외회전에서 불안감 확인, 후방 지지 시 완화 확인.",
        positive="통증보다 ‘빠질 것 같은 불안감’이 핵심."
    ),
    "Sulcus": PhysicalTest(
        name="🧪 Sulcus Sign",
        target="하방/다방향 불안정",
        how="팔을 아래로 견인해 견봉 아래 함몰(sulcus) 관찰.",
        positive="뚜렷한 함몰 + 증상 재현."
    ),
    "ApleyScratch": PhysicalTest(
        name="🧪 Apley Scratch / ROM",
        target="가동범위 제한(동결견 등)",
        how="손을 머리 뒤/등 뒤로 보내며 내·외회전 기능 비교.",
        positive="좌우 차이 크게 감소, 특히 외회전 제한."
    ),
    "Spurling": PhysicalTest(
        name="🧪 Spurling (Neck Screen)",
        target="경추성 방사통(신경근)",
        how="목 신전+측굴 후 축성 압박으로 방사통 재현 여부.",
        positive="팔/손으로 뻗치는 방사통 재현.",
        caution="진행성 근력저하/감각저하 시 정밀평가 권고."
    ),
}

EXERCISES: Dict[str, Exercise] = {
    "Pendulum": Exercise(
        name="🌀 Pendulum (Codman)",
        goal="통증 완화 + 부담 최소 가동성 확보",
        steps=[
            "🧍‍♂️ 상체를 살짝 숙이고, 건강한 팔로 지지해요.",
            "🧎‍♂️ 아픈 팔은 힘을 빼고 아래로 늘어뜨려요.",
            "🌀 작은 원/좌우/앞뒤로 ‘가볍게’ 흔들어요."
        ],
        dosage="⏱️ 30–60초 × 2–3세트, 하루 1–3회 (통증 범위 내)",
        svg=SVG_PENDULUM,
        cautions="⚠️ 찌르는 통증이면 범위를 줄이거나 중단."
    ),
    "ScapRetraction": Exercise(
        name="🪽 Scapular Retraction",
        goal="견갑 안정화로 충돌·과부하 완화 보조",
        steps=[
            "🧘 어깨 힘을 빼고 목을 길게 만들어요.",
            "🪽 날개뼈를 ‘뒤로 + 아래로’ 살짝 모아요(으쓱 금지!).",
            "🧊 2–3초 유지 → 천천히 풀어요."
        ],
        dosage="🔁 10–15회 × 2–3세트, 주 4–6일",
        svg=SVG_SCAP_RETRACT,
        cautions="⚠️ 승모근으로 으쓱하면 강도를 낮추세요."
    ),
    "ExternalRotation": Exercise(
        name="🧲 External Rotation (Band/Isometric)",
        goal="회전근개 강화로 통증·불안정 개선",
        steps=[
            "🧻 팔꿈치 옆구리에 수건을 끼우면 자세 유지가 쉬워요.",
            "🧲 밴드를 잡고 손을 ‘바깥으로’ 천천히 이동해요.",
            "🐢 끝범위 1초 정지 → 천천히 돌아와요."
        ],
        dosage="💪 8–12회 × 2–3세트, 주 3–5일",
        svg=SVG_ER_BAND,
        cautions="⚠️ 통증이 크면 밴드 대신 ‘가벼운 버티기(등척성)’부터."
    ),
    "DoorwayStretch": Exercise(
        name="🚪 Doorway Stretch",
        goal="흉근 긴장 완화 → 어깨 말림 개선 보조",
        steps=[
            "🚪 문틀에 팔을 걸치고 한 발 앞으로 나가요.",
            "🫁 가슴이 ‘부드럽게’ 늘어나는 정도까지만 이동해요.",
            "⏳ 20–30초 유지하며 호흡을 편하게 해요."
        ],
        dosage="🧘 20–30초 × 2–3회, 하루 1–2회",
        svg=SVG_DOORWAY,
        cautions="⚠️ 앞쪽 어깨가 콕 찌르면 팔 위치를 낮추거나 중단."
    ),
}

SYMPTOMS: Dict[str, Dict] = {
    "🙋‍♂️ 팔을 올릴 때(특히 60–120°) 아픈 ‘통증호’": {
        "tags": ["🎯 견봉하 충돌", "🧵 회전근개 과사용"],
        "tests": ["PainfulArc", "Neer", "Hawkins", "EmptyCan"],
        "exercises": ["Pendulum", "ScapRetraction", "ExternalRotation", "DoorwayStretch"]
    },
    "🌙 야간통/누우면 악화(옆으로 눕기 힘듦)": {
        "tags": ["🧵 회전근개 병변", "💧 점액낭/염증"],
        "tests": ["Neer", "Hawkins", "EmptyCan", "DropArm"],
        "exercises": ["Pendulum", "ScapRetraction", "ExternalRotation"]
    },
    "💪 힘이 빠짐/물건 들기 어렵고 ‘툭’ 떨어질 듯함": {
        "tags": ["🧵 파열/기능저하 가능", "📉 근력 저하"],
        "tests": ["EmptyCan", "DropArm", "ERLag", "LiftOff", "BellyPress"],
        "exercises": ["Pendulum", "ScapRetraction", "ExternalRotation"]
    },
    "👉 앞쪽 어깨 통증 + 이두구 콕콕(팔 들 때 앞쪽 통증)": {
        "tags": ["🧷 이두근 장두", "🧩 SLAP 가능"],
        "tests": ["Speed", "Yergason", "OBrien"],
        "exercises": ["ScapRetraction", "ExternalRotation", "DoorwayStretch"]
    },
    "😨 ‘빠질 것 같은’ 불안감/탈구 병력": {
        "tags": ["🧨 전방/다방향 불안정"],
        "tests": ["Apprehension", "Sulcus"],
        "exercises": ["ScapRetraction", "ExternalRotation"]
    },
    "🧊 어깨가 전반적으로 뻣뻣(특히 외회전) + ROM 감소": {
        "tags": ["🧊 동결견 가능", "📏 가동범위 제한"],
        "tests": ["ApleyScratch"],
        "exercises": ["Pendulum", "DoorwayStretch"]
    },
    "⚡ 목/팔로 뻗치는 저림·방사통(손까지)": {
        "tags": ["🧠 경추성 통증/신경근"],
        "tests": ["Spurling"],
        "exercises": ["ScapRetraction", "DoorwayStretch"]
    },
    "📍 어깨 위(쇄골 끝) 국소 통증(AC joint 쪽)": {
        "tags": ["🔩 AC joint"],
        "tests": ["CrossBody", "OBrien"],
        "exercises": ["ScapRetraction", "DoorwayStretch"]
    },
}

# =============================
# Hero
# =============================
st.markdown(
    """
<div class="hero">
  <h1 class="hero-title">🌈 어깨 통증 이학적 검사 & 운동 가이드 🦴✨</h1>
  <div class="hero-sub">
    🎓 교육용 요약 도구예요. <b>증상 선택 👉 검사 방법/양성 소견 👉 기본 운동(그림)</b>을 한 번에 보여줘요.<br/>
    ⚠️ 진단 확정은 병력·ROM·촉진·신경학적 검사 및 필요 시 영상검사를 함께 고려해야 해요.
  </div>
</div>
""",
    unsafe_allow_html=True
)

st.write("")

# =============================
# Safety
# =============================
with st.expander("🚨 레드플래그(이 경우 ‘자가검사’보다 ‘진료’가 먼저예요!)"):
    st.markdown(
        """
- 🧨 외상 후 변형/탈구 의심, 팔을 거의 못 움직일 정도의 급성 통증  
- 🌡️ 발열/오한/전신 증상 + 어깨 통증(감염 가능성)  
- 🧠 진행성 근력저하/감각저하, 손이 차갑거나 색 변화  
- 🧬 암 병력/원인불명 체중감소/야간에 점점 심해지는 통증  
"""
    )

# =============================
# Layout
# =============================
left, right = st.columns([0.36, 0.64], gap="large")

with left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title grad-text'>🧩 1) 증상 선택</div>", unsafe_allow_html=True)

    symptom = st.selectbox("어떤 증상이 가장 주된가요? 🤔", list(SYMPTOMS.keys()))
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

    st.markdown("<div class='section-title grad-text'>🧷 2) 체크(선택)</div>", unsafe_allow_html=True)
    trauma = st.checkbox("🧨 최근 외상(넘어짐/부딪힘/무거운 물건) 있었어요")
    fever = st.checkbox("🌡️ 발열/오한/전신 컨디션 저하가 있어요")
    neuro = st.checkbox("⚡ 손 저림/감각저하/힘 빠짐이 진행 중이에요")

    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    go = st.button("🚀 검사 & 운동 보기")

    st.markdown(
        "<div class='small'>📝 이 앱은 교육용이에요. 검사 중 통증이 과하면 즉시 중단하세요.</div>",
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    cfg = SYMPTOMS[symptom]

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title grad-text'>✨ 요약 카드</div>", unsafe_allow_html=True)
    st.markdown(f"**선택한 증상:** {symptom}")
    st.markdown("**관련 키워드:**")
    st.markdown(chips(cfg["tags"]), unsafe_allow_html=True)

    alerts = []
    if trauma:
        alerts.append("🧨 외상 후라면 골절/탈구/파열 평가가 필요할 수 있어요.")
    if fever:
        alerts.append("🌡️ 발열 동반 시 감염성 원인 배제가 우선이에요.")
    if neuro:
        alerts.append("⚡ 진행성 저림/근력저하는 신경학적 평가를 권장해요.")
    if alerts:
        st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
        st.warning(" ".join(alerts))

    st.markdown("</div>", unsafe_allow_html=True)

    # 3) Tests
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title grad-text'>🧪 3) 이학적 검사(방법 & 양성 소견)</div>", unsafe_allow_html=True)
    st.markdown("<div class='note'>💡 한 번에 여러 검사가 ‘같이’ 양성이 나올 수 있어요. 통증이 심하면 범위를 줄여요.</div>", unsafe_allow_html=True)
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

    tests_to_show = cfg["tests"]
    for key in tests_to_show:
        t = TESTS[key]
        with st.expander(f"{t.name}  |  🎯 {t.target}"):
            st.markdown(f"**🧭 방법:** {wrap(t.how)}")
            st.markdown(f"**✅ 양성:** {wrap(t.positive)}")
            if t.caution:
                st.markdown(f"**⚠️ 주의:** {wrap(t.caution)}")

    st.markdown("</div>", unsafe_allow_html=True)

    # 4) Exercises
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title grad-text'>🏋️ 4) 운동(간단 그림 포함)</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='note'>✨ 원칙: <b>통증 범위 내</b> + <b>다음 날 통증이 확 증가하면</b> 강도/횟수를 줄이세요.</div>",
        unsafe_allow_html=True
    )
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

    ex_to_show = cfg["exercises"]

    for key in ex_to_show:
        ex = EXERCISES[key]
        cols = st.columns([0.56, 0.44], gap="medium")

        with cols[0]:
            st.markdown(f"### {ex.name} 🌟")
            st.markdown(f"**🎯 목적:** {ex.goal}")
            st.markdown("**🪄 방법:**")
            for s in ex.steps:
                st.markdown(f"- {s}")
            st.markdown(f"**📌 권장량:** {ex.dosage}")
            if ex.cautions:
                st.markdown(f"**⚠️ 주의:** {ex.cautions}")

        with cols[1]:
            st.markdown(svg_card(ex.svg), unsafe_allow_html=True)

        st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.write("")
st.markdown(
    "<div class='note' style='text-align:center;'>💙 Made with Streamlit | 🌼 White background + colorful accents | 🧠 Educational use only</div>",
    unsafe_allow_html=True
)
