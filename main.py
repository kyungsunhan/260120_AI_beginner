import streamlit as st
from dataclasses import dataclass
from typing import List, Dict, Optional
import textwrap

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Shoulder Exam Helper",
    page_icon="🦴",
    layout="wide",
)

# -----------------------------
# Minimal white/blue CSS
# -----------------------------
CSS = """
<style>
.stApp { background:#F7FAFF; color:#0B1B3A; }
html, body, [class*="css"]  {
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, "Noto Sans KR", "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
}
.header {
  background: linear-gradient(90deg, #0B63F6 0%, #2EA8FF 100%);
  padding: 16px 18px;
  border-radius: 14px;
  color: white;
  box-shadow: 0 10px 26px rgba(11,99,246,0.18);
}
.header h1{ margin:0; font-size: 24px; font-weight: 900; letter-spacing:-0.3px; }
.header p{ margin:6px 0 0 0; font-size: 13px; opacity:0.92; line-height:1.35; }
.card {
  background: #FFFFFF;
  border: 1px solid rgba(11, 99, 246, 0.12);
  border-radius: 14px;
  padding: 14px 14px 10px 14px;
  box-shadow: 0 8px 22px rgba(17, 34, 68, 0.06);
}
.card + .card { margin-top: 12px; }
.section-title{
  font-size: 15px;
  font-weight: 900;
  color: #083A99;
  margin: 0 0 10px 0;
}
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
.hr { height: 1px; background: rgba(11, 99, 246, 0.12); margin: 12px 0; }
.note { color: rgba(11, 27, 58, 0.72); font-size: 13px; line-height: 1.5; }
.small { color: rgba(11, 27, 58, 0.72); font-size: 12.5px; line-height: 1.5; }
div.stButton > button {
  background: #0B63F6; color: white; font-weight: 900;
  border: 1px solid rgba(11, 99, 246, 0.35);
  border-radius: 12px; padding: 0.7rem 1.0rem;
  box-shadow: 0 10px 22px rgba(11,99,246,0.18);
}
div.stButton > button:hover { background:#0957D8; }
[data-baseweb="select"] > div {
  background:#FFFFFF !important;
  border-radius:12px !important;
  border: 1px solid rgba(11, 99, 246, 0.18) !important;
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# -----------------------------
# Models
# -----------------------------
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

def wrap_md(s: str) -> str:
    return "\n".join(textwrap.wrap(s, width=88))

# -----------------------------
# Simple SVG library (very basic diagrams)
# -----------------------------
def svg_card(svg: str, height: int = 180) -> str:
    return f"""
    <div style="border:1px solid rgba(11,99,246,0.12); border-radius:12px; background: rgba(11,99,246,0.03); padding:10px;">
      <div style="max-width:100%; overflow:hidden;">
        {svg}
      </div>
    </div>
    """

SVG_PENDULUM = """
<svg width="520" height="180" viewBox="0 0 520 180" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="520" height="180" rx="12" fill="white"/>
  <text x="18" y="26" font-size="14" font-weight="700" fill="#083A99">Pendulum (Codman) - 팔 흔들기</text>

  <!-- table -->
  <rect x="40" y="72" width="190" height="12" rx="6" fill="#0B63F6" opacity="0.25"/>

  <!-- torso leaning -->
  <circle cx="95" cy="62" r="10" fill="#0B63F6" opacity="0.85"/>
  <line x1="95" y1="72" x2="120" y2="110" stroke="#0B63F6" stroke-width="6" stroke-linecap="round"/>
  <line x1="120" y1="110" x2="155" y2="120" stroke="#0B63F6" stroke-width="6" stroke-linecap="round"/>

  <!-- support arm to table -->
  <line x1="120" y1="110" x2="80" y2="78" stroke="#0B63F6" stroke-width="5" stroke-linecap="round" opacity="0.85"/>

  <!-- hanging arm -->
  <line x1="155" y1="120" x2="175" y2="150" stroke="#0B63F6" stroke-width="6" stroke-linecap="round"/>
  <circle cx="175" cy="150" r="6" fill="#0B63F6" opacity="0.9"/>

  <!-- swing arcs -->
  <path d="M175 150 C205 140, 220 125, 230 110" fill="none" stroke="#2EA8FF" stroke-width="3" stroke-dasharray="6 6"/>
  <path d="M175 150 C150 140, 135 125, 125 110" fill="none" stroke="#2EA8FF" stroke-width="3" stroke-dasharray="6 6"/>
  <text x="255" y="122" font-size="12" fill="#0B1B3A" opacity="0.75">작게 원/좌우로 흔들기</text>

  <!-- notes -->
  <text x="300" y="150" font-size="12" fill="#0B1B3A" opacity="0.75">통증 범위 내에서</text>
</svg>
"""

SVG_SCAP_RETRACT = """
<svg width="520" height="180" viewBox="0 0 520 180" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="520" height="180" rx="12" fill="white"/>
  <text x="18" y="26" font-size="14" font-weight="700" fill="#083A99">Scapular Retraction - 견갑골 모으기</text>

  <!-- person back -->
  <circle cx="130" cy="60" r="10" fill="#0B63F6" opacity="0.85"/>
  <line x1="130" y1="70" x2="130" y2="130" stroke="#0B63F6" stroke-width="8" stroke-linecap="round"/>
  <line x1="110" y1="92" x2="150" y2="92" stroke="#0B63F6" stroke-width="6" stroke-linecap="round" opacity="0.9"/>

  <!-- shoulder blades -->
  <path d="M115 108 Q130 95 145 108" fill="none" stroke="#2EA8FF" stroke-width="4"/>
  <path d="M115 118 Q130 105 145 118" fill="none" stroke="#2EA8FF" stroke-width="4"/>

  <!-- arrows inward -->
  <line x1="85" y1="112" x2="110" y2="112" stroke="#2EA8FF" stroke-width="3"/>
  <polygon points="110,112 103,108 103,116" fill="#2EA8FF"/>
  <line x1="175" y1="112" x2="150" y2="112" stroke="#2EA8FF" stroke-width="3"/>
  <polygon points="150,112 157,108 157,116" fill="#2EA8FF"/>

  <text x="220" y="85" font-size="12" fill="#0B1B3A" opacity="0.75">어깨를 으쓱하지 말고</text>
  <text x="220" y="105" font-size="12" fill="#0B1B3A" opacity="0.75">날개뼈를 뒤로 ‘모으기’</text>
</svg>
"""

SVG_ER_BAND = """
<svg width="520" height="180" viewBox="0 0 520 180" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="520" height="180" rx="12" fill="white"/>
  <text x="18" y="26" font-size="14" font-weight="700" fill="#083A99">External Rotation - 외회전 밴드</text>

  <!-- torso -->
  <circle cx="120" cy="58" r="10" fill="#0B63F6" opacity="0.85"/>
  <line x1="120" y1="68" x2="120" y2="132" stroke="#0B63F6" stroke-width="8" stroke-linecap="round"/>

  <!-- arm at 90 elbow -->
  <line x1="120" y1="92" x2="160" y2="92" stroke="#0B63F6" stroke-width="6" stroke-linecap="round"/>
  <line x1="160" y1="92" x2="160" y2="120" stroke="#0B63F6" stroke-width="6" stroke-linecap="round"/>

  <!-- towel -->
  <rect x="118" y="98" width="10" height="18" rx="4" fill="#2EA8FF" opacity="0.5"/>
  <text x="185" y="98" font-size="12" fill="#0B1B3A" opacity="0.75">팔꿈치 옆에 수건</text>

  <!-- band anchor -->
  <circle cx="260" cy="92" r="6" fill="#0B63F6" opacity="0.85"/>
  <line x1="260" y1="92" x2="160" y2="110" stroke="#2EA8FF" stroke-width="4"/>
  <text x="270" y="95" font-size="12" fill="#0B1B3A" opacity="0.75">밴드 고정</text>

  <!-- rotation arrow -->
  <path d="M165 122 A30 30 0 0 0 195 112" fill="none" stroke="#2EA8FF" stroke-width="3"/>
  <polygon points="195,112 188,110 190,117" fill="#2EA8FF"/>
  <text x="220" y="130" font-size="12" fill="#0B1B3A" opacity="0.75">손을 바깥으로 천천히</text>
</svg>
"""

SVG_DOORWAY_STRETCH = """
<svg width="520" height="180" viewBox="0 0 520 180" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="520" height="180" rx="12" fill="white"/>
  <text x="18" y="26" font-size="14" font-weight="700" fill="#083A99">Doorway Stretch - 흉근 스트레칭</text>

  <!-- doorway -->
  <rect x="300" y="48" width="22" height="110" fill="#0B63F6" opacity="0.25"/>
  <rect x="420" y="48" width="22" height="110" fill="#0B63F6" opacity="0.25"/>
  <rect x="300" y="48" width="142" height="18" fill="#0B63F6" opacity="0.25"/>

  <!-- person -->
  <circle cx="140" cy="68" r="10" fill="#0B63F6" opacity="0.85"/>
  <line x1="140" y1="78" x2="140" y2="140" stroke="#0B63F6" stroke-width="8" stroke-linecap="round"/>
  <line x1="140" y1="95" x2="190" y2="80" stroke="#0B63F6" stroke-width="6" stroke-linecap="round"/>
  <line x1="140" y1="95" x2="190" y2="110" stroke="#0B63F6" stroke-width="6" stroke-linecap="round"/>

  <!-- arms to doorway -->
  <line x1="190" y1="80" x2="300" y2="68" stroke="#2EA8FF" stroke-width="3" stroke-dasharray="6 6"/>
  <line x1="190" y1="110" x2="300" y2="120" stroke="#2EA8FF" stroke-width="3" stroke-dasharray="6 6"/>

  <!-- forward arrow -->
  <line x1="165" y1="150" x2="210" y2="150" stroke="#2EA8FF" stroke-width="3"/>
  <polygon points="210,150 203,146 203,154" fill="#2EA8FF"/>
  <text x="220" y="154" font-size="12" fill="#0B1B3A" opacity="0.75">가슴을 앞으로</text>
</svg>
"""

# -----------------------------
# Test Library (핵심만 간결하게)
# -----------------------------
TESTS: Dict[str, PhysicalTest] = {
    "Neer": PhysicalTest(
        name="Neer Impingement",
        target="견봉하 충돌/회전근개 병변(충돌 기전)",
        how="견갑을 고정한 뒤, 팔을 내회전 상태로 전방거상(끝범위까지)합니다.",
        positive="전외측 어깨 통증/불편감 재현(특히 70–120° 부근 또는 끝범위).",
        caution="급성 통증이 매우 심하면 범위를 줄이거나 중단."
    ),
    "Hawkins": PhysicalTest(
        name="Hawkins-Kennedy",
        target="견봉하 충돌",
        how="어깨 90° 굴곡 + 팔꿈치 90° 굴곡 후, 전완을 내회전시킵니다.",
        positive="전외측 어깨 통증 재현."
    ),
    "PainfulArc": PhysicalTest(
        name="Painful Arc",
        target="견봉하 충돌/상완골두-견봉 사이 문제",
        how="팔을 외전(옆으로 올리기)하며 통증 구간을 확인합니다.",
        positive="대개 60–120° 구간에서 통증 증가 후, 그 이상에서 감소."
    ),
    "EmptyCan": PhysicalTest(
        name="Empty Can (Jobe)",
        target="극상근(supraspinatus) 관련",
        how="어깨 90° 외전+30° 전방(Scaption)에서 엄지를 아래(내회전)로 하고 저항을 줍니다.",
        positive="통증 또는 근력 저하(좌우 비교).",
        caution="심한 통증이면 Full Can(엄지 위)로 대체 고려."
    ),
    "DropArm": PhysicalTest(
        name="Drop Arm",
        target="전층 회전근개 파열(특히 극상근)",
        how="팔을 외전시킨 뒤 천천히 내리게 합니다.",
        positive="버티지 못하고 갑자기 떨어짐/심한 통증으로 조절 불가."
    ),
    "ERLag": PhysicalTest(
        name="External Rotation Lag Sign",
        target="극하근/소원근(후방 회전근개) 파열 가능",
        how="팔꿈치 90° 굴곡, 어깨 외회전 최대로 위치시킨 후 ‘유지’하도록 합니다.",
        positive="외회전 유지 못하고 내회전으로 ‘흘러내림’."
    ),
    "LiftOff": PhysicalTest(
        name="Lift-off",
        target="견갑하근(subscapularis) 기능",
        how="손등을 허리 뒤에 두고(내회전), 손을 등에서 떼어 올리게 합니다.",
        positive="손을 떼지 못함/약함/통증."
    ),
    "BellyPress": PhysicalTest(
        name="Belly-press",
        target="견갑하근 대체 검사",
        how="손바닥을 복부에 대고 팔꿈치를 앞으로 유지한 채 복부를 누릅니다.",
        positive="팔꿈치가 뒤로 빠지거나(보상), 힘/통증 문제."
    ),
    "Speed": PhysicalTest(
        name="Speed Test",
        target="상완이두근 장두/SLAP 의심",
        how="팔을 90° 전방거상, 팔꿈치 신전, 전완 회외 상태에서 아래로 누르는 저항을 버팁니다.",
        positive="이두구(bicipital groove) 통증."
    ),
    "Yergason": PhysicalTest(
        name="Yergason",
        target="이두근 장두/횡상완인대",
        how="팔꿈치 90° 굴곡, 전완 회외 + 외회전에 저항을 줍니다.",
        positive="이두구 통증/불안정 느낌."
    ),
    "OBrien": PhysicalTest(
        name="O'Brien (Active Compression)",
        target="SLAP/AC joint",
        how="어깨 90° 굴곡, 10–15° 내전, 엄지 아래로(내회전) 저항 → 엄지 위(외회전)로 반복.",
        positive="내회전에서 통증↑, 외회전에서 감소(또는 위치에 따른 통증 양상)."
    ),
    "CrossBody": PhysicalTest(
        name="Cross-body Adduction",
        target="AC joint(견봉쇄골관절) 병변",
        how="팔을 90° 굴곡 후, 몸통 쪽으로 가로질러 내전합니다.",
        positive="AC joint 부위 국소 통증."
    ),
    "Apprehension": PhysicalTest(
        name="Apprehension/Relocation",
        target="전방 불안정/재발성 탈구",
        how="어깨 외전+외회전에서 ‘불안/두려움’(Apprehension) 확인, 후방으로 밀어(Relocation) 완화되는지 봅니다.",
        positive="통증보다 ‘빠질 것 같은 불안감’이 핵심."
    ),
    "Sulcus": PhysicalTest(
        name="Sulcus Sign",
        target="하방/다방향 불안정",
        how="팔을 늘어뜨린 상태에서 아래로 견인하여 견봉 아래 함몰(sulcus) 관찰.",
        positive="뚜렷한 함몰 + 증상 재현."
    ),
    "ApleyScratch": PhysicalTest(
        name="Apley Scratch / ROM",
        target="가동범위 제한(동결견 등)",
        how="손을 머리 뒤/등 뒤로 보내는 동작으로 외회전·내회전 기능을 대략 확인합니다.",
        positive="좌우 차이 크게 감소, 특히 외회전 제한이 두드러짐."
    ),
    "Spurling": PhysicalTest(
        name="Spurling (Neck Screen)",
        target="경추성 방사통(신경근)",
        how="목을 신전+측굴 후 축성 압박으로 방사통 재현 여부 확인.",
        positive="팔/손으로 뻗치는 방사통 재현.",
        caution="신경학적 증상(근력저하/감각저하)이 동반되면 정밀평가 권고."
    ),
}

# -----------------------------
# Exercise Library (핵심 운동 + 간단 그림)
# -----------------------------
EXERCISES: Dict[str, Exercise] = {
    "Pendulum": Exercise(
        name="Pendulum (Codman)",
        goal="통증 완화 + 관절 부담 최소로 가벼운 가동성 확보",
        steps=[
            "건강한 팔로 지지하고 상체를 살짝 숙입니다.",
            "아픈 팔은 힘을 빼고 아래로 늘어뜨립니다.",
            "작게 앞/뒤 또는 좌/우로 흔들거나 작은 원을 그립니다."
        ],
        dosage="30–60초 × 2–3세트, 하루 1–3회 (통증 범위 내)",
        svg=SVG_PENDULUM,
        cautions="통증이 날카롭게 증가하면 범위를 줄이거나 중단."
    ),
    "ScapRetraction": Exercise(
        name="Scapular Retraction",
        goal="견갑 안정화(자세/견갑 컨트롤)로 충돌·과부하 완화",
        steps=[
            "의자에 앉거나 선 자세에서 어깨 힘을 빼고 목을 길게 합니다.",
            "날개뼈를 ‘뒤로, 아래로’ 가볍게 모읍니다(으쓱 금지).",
            "2–3초 유지 후 천천히 이완합니다."
        ],
        dosage="10–15회 × 2–3세트, 주 4–6일",
        svg=SVG_SCAP_RETRACT,
        cautions="승모근 상부로 으쓱하는 보상이 나오면 강도를 낮추세요."
    ),
    "ExternalRotation": Exercise(
        name="External Rotation (Band or Isometric)",
        goal="회전근개(특히 후방) 강화로 통증·불안정 개선",
        steps=[
            "팔꿈치를 옆구리에 붙이고(수건 끼우면 도움) 90° 굴곡합니다.",
            "밴드를 당겨 손을 바깥으로 천천히 이동합니다.",
            "끝범위에서 1초 정지 후 천천히 돌아옵니다."
        ],
        dosage="8–12회 × 2–3세트, 주 3–5일",
        svg=SVG_ER_BAND,
        cautions="통증이 심하면 밴드 대신 ‘가벼운 등척성(밀기/버티기)’로 시작."
    ),
    "DoorwayStretch": Exercise(
        name="Doorway Stretch",
        goal="흉근/전면 구조 긴장 완화 → 어깨 전방화(말림) 개선 보조",
        steps=[
            "문틀에 팔을 걸치고(편한 높이) 한 발 앞으로 나갑니다.",
            "가슴이 부드럽게 늘어나는 정도까지만 체중을 싣습니다.",
            "호흡을 유지하며 20–30초 유지합니다."
        ],
        dosage="20–30초 × 2–3회, 하루 1–2회",
        svg=SVG_DOORWAY_STRETCH,
        cautions="앞쪽 어깨가 찌르는 통증이면 팔 위치를 낮추거나 중단."
    ),
}

# -----------------------------
# Symptom → Suggested tests/exercises mapping
# -----------------------------
SYMPTOMS: Dict[str, Dict] = {
    "팔을 올릴 때(특히 60–120°) 아픈 ‘통증호(통증구간)’": {
        "tags": ["견봉하 충돌", "회전근개 과사용"],
        "tests": ["PainfulArc", "Neer", "Hawkins", "EmptyCan"],
        "exercises": ["Pendulum", "ScapRetraction", "ExternalRotation", "DoorwayStretch"]
    },
    "야간통/누우면 악화(특히 옆으로 눕기 힘듦)": {
        "tags": ["회전근개 병변", "염증/점액낭"],
        "tests": ["Neer", "Hawkins", "EmptyCan", "DropArm"],
        "exercises": ["Pendulum", "ScapRetraction", "ExternalRotation"]
    },
    "힘이 빠짐/물건 들기 어렵고 ‘툭’ 떨어질 듯함": {
        "tags": ["회전근개 파열 가능", "근력저하"],
        "tests": ["EmptyCan", "DropArm", "ERLag", "LiftOff", "BellyPress"],
        "exercises": ["Pendulum", "ScapRetraction", "ExternalRotation"]
    },
    "앞쪽 어깨 통증 + 팔 들면 앞쪽이 콕콕 / 이두구 통증": {
        "tags": ["이두근 장두", "SLAP 가능"],
        "tests": ["Speed", "Yergason", "OBrien"],
        "exercises": ["ScapRetraction", "ExternalRotation", "DoorwayStretch"]
    },
    "어깨 앞쪽이 ‘빠질 것 같은’ 불안감/탈구 병력": {
        "tags": ["전방/다방향 불안정"],
        "tests": ["Apprehension", "Sulcus"],
        "exercises": ["ScapRetraction", "ExternalRotation"]
    },
    "어깨가 전반적으로 뻣뻣하고(특히 외회전) 가동범위가 줄어듦": {
        "tags": ["동결견(유착성 관절낭염) 가능", "가동범위 제한"],
        "tests": ["ApleyScratch"],
        "exercises": ["Pendulum", "DoorwayStretch"]
    },
    "목/팔로 뻗치는 저림·방사통(손까지 내려감)": {
        "tags": ["경추성 통증/신경근"],
        "tests": ["Spurling"],
        "exercises": ["ScapRetraction", "DoorwayStretch"]  # 목/신경가동 등은 안전상 여기서는 최소화
    },
    "견봉쇄골관절(어깨 위/쇄골 끝) 국소 통증": {
        "tags": ["AC joint"],
        "tests": ["CrossBody", "OBrien"],
        "exercises": ["ScapRetraction", "DoorwayStretch"]
    },
}

# -----------------------------
# Header
# -----------------------------
st.markdown(
    """
<div class="header">
  <h1>어깨 통증 이학적 검사 & 운동 도우미 🦴</h1>
  <p>교육용 요약 도구입니다. 증상 선택 → 관련 이학적 검사(방법/양성 소견) → 기본 운동(간단 그림) 제공</p>
</div>
""",
    unsafe_allow_html=True
)

st.write("")

# -----------------------------
# Safety / Red flags
# -----------------------------
with st.expander("⚠️ 안전 안내(레드 플래그 / 즉시 평가 권고)"):
    st.markdown(
        """
- **외상 후 변형/탈구 의심**, 팔을 거의 못 움직일 정도의 급성 통증  
- **휴식 시에도 지속되는 심한 통증**, **발열/오한**, 심한 전신 증상  
- **팔/손의 진행성 근력저하**, 감각소실, 손이 심하게 차가워짐/색 변화  
- **암 병력**, 원인 불명 체중 감소, 야간에 점점 심해지는 통증  
위 항목이 있으면 자가검사보다 **대면 진료/영상 평가**를 우선하세요.
"""
    )

# -----------------------------
# Layout
# -----------------------------
left, right = st.columns([0.36, 0.64], gap="large")

with left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>1) 주요 증상 선택</div>", unsafe_allow_html=True)

    symptom = st.selectbox("가장 주된 증상을 고르세요", list(SYMPTOMS.keys()))
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>2) 체크(선택)</div>", unsafe_allow_html=True)
    trauma = st.checkbox("최근 외상(넘어짐/부딪힘/무거운 물건 들다 삐끗함)이 있었음")
    fever = st.checkbox("발열/오한/전신 컨디션 저하가 동반됨")
    neuro = st.checkbox("손 저림/감각저하/힘 빠짐이 진행 중")

    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    go = st.button("검사/운동 제시")

    st.markdown(
        "<div class='small'>※ 본 앱은 진단이 아닌 교육용 안내입니다. 실제 임상에서는 병력·ROM·촉진·신경학적 검사 및 필요 시 영상검사와 함께 판단합니다.</div>",
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    cfg = SYMPTOMS[symptom]

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>요약</div>", unsafe_allow_html=True)
    st.markdown(f"**선택 증상:** {symptom}")
    st.markdown("**관련 키워드:**")
    st.markdown(chips([f"🔹 {t}" for t in cfg["tags"]]), unsafe_allow_html=True)

    # Quick safety messages based on checks
    alerts = []
    if trauma:
        alerts.append("외상 후 증상이라면 골절/탈구/파열 평가가 필요할 수 있습니다.")
    if fever:
        alerts.append("발열/전신 증상 동반 시 감염성 원인 배제가 우선입니다.")
    if neuro:
        alerts.append("진행성 저림/근력저하는 신경학적 평가를 권고합니다.")
    if alerts:
        st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
        st.warning(" ".join(alerts))
    st.markdown("</div>", unsafe_allow_html=True)

    # Show tests & exercises when button clicked; otherwise still show concise preview
    tests_to_show = cfg["tests"]
    ex_to_show = cfg["exercises"]

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>3) 추천 이학적 검사</div>", unsafe_allow_html=True)

    for key in tests_to_show:
        t = TESTS[key]
        with st.expander(f"🧪 {t.name} — {t.target}"):
            st.markdown(f"**방법:** {wrap_md(t.how)}")
            st.markdown(f"**양성 소견:** {wrap_md(t.positive)}")
            if t.caution:
                st.markdown(f"**주의:** {wrap_md(t.caution)}")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>4) 기본 운동(간단 그림)</div>", unsafe_allow_html=True)
    st.markdown("<div class='note'>원칙: 통증 범위 내에서 시작하고, 다음 날 통증이 확 올라가면 강도/횟수를 줄이세요.</div>", unsafe_allow_html=True)
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

    for key in ex_to_show:
        ex = EXERCISES[key]
        cols = st.columns([0.55, 0.45], gap="medium")
        with cols[0]:
            st.markdown(f"**{ex.name}**")
            st.markdown(f"- 목적: {ex.goal}")
            st.markdown("- 방법:")
            for s in ex.steps:
                st.markdown(f"  - {s}")
            st.markdown(f"- 권장: {ex.dosage}")
            if ex.cautions:
                st.markdown(f"- 주의: {ex.cautions}")
        with cols[1]:
            st.markdown(svg_card(ex.svg), unsafe_allow_html=True)

        st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.write("")
st.markdown(
    "<div class='note' style='text-align:center;'>© Shoulder Exam Helper — Educational Use Only</div>",
    unsafe_allow_html=True
)
