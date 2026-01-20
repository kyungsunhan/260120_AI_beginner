import streamlit as st
from dataclasses import dataclass
from typing import List, Optional, Tuple
from urllib.parse import quote

# =========================
# Page
# =========================
st.set_page_config(
    page_title="⛷️ 옥수동 3시간 이내 스키장",
    page_icon="❄️",
    layout="wide",
)

# =========================
# Flashy (white background)
# =========================
CSS = """
<style>
.stApp { background:#ffffff; color:#101828; }
html, body, [class*="css"]{
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, "Noto Sans KR",
               "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
}

/* Hero */
.hero{
  border-radius: 18px;
  padding: 18px 20px;
  background:
    radial-gradient(circle at 12% 20%, rgba(255, 88, 174, 0.22), transparent 40%),
    radial-gradient(circle at 88% 20%, rgba(0, 209, 255, 0.20), transparent 42%),
    radial-gradient(circle at 30% 90%, rgba(0, 255, 187, 0.14), transparent 45%),
    linear-gradient(90deg, #0B63F6 0%, #2EA8FF 45%, #7C3AED 100%);
  color: white;
  box-shadow: 0 16px 44px rgba(12, 74, 255, 0.18);
}
.hero h1{
  margin:0;
  font-size: 28px;
  font-weight: 900;
  letter-spacing: -0.4px;
  text-shadow: 0 10px 28px rgba(0,0,0,0.25);
}
.hero p{
  margin: 6px 0 0 0;
  font-size: 13.5px;
  opacity: 0.95;
  line-height: 1.5;
}

/* Cards */
.card{
  background: rgba(255,255,255,0.95);
  border: 1px solid rgba(15, 23, 42, 0.10);
  border-radius: 18px;
  padding: 16px 16px 12px 16px;
  box-shadow: 0 14px 40px rgba(2, 6, 23, 0.08);
}
.card + .card { margin-top: 14px; }

.section-title{
  font-size: 15px;
  font-weight: 900;
  margin: 0 0 10px 0;
}
.grad-text{
  background: linear-gradient(90deg, #0B63F6, #2EA8FF, #7C3AED, #FF58AE);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

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

.hr{
  height: 1px;
  margin: 12px 0;
  background: linear-gradient(90deg, transparent, rgba(11,99,246,0.25), rgba(255,88,174,0.25), transparent);
}

.note{
  color: rgba(16,24,40,0.72);
  font-size: 13px;
  line-height: 1.55;
}

/* Button */
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

[data-baseweb="select"] > div{
  background:#ffffff !important;
  border-radius:14px !important;
  border: 1px solid rgba(11, 99, 246, 0.18) !important;
  box-shadow: 0 10px 22px rgba(2, 6, 23, 0.05);
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# =========================
# Data model
# =========================
@dataclass
class Resort:
    name: str
    region: str
    highlights: List[str]
    # Minutes (rough typical)
    car_min: Optional[Tuple[int, int]] = None          # (min, max)
    public_min: Optional[Tuple[int, int]] = None       # (min, max) bus/subway
    ktx_min: Optional[Tuple[int, int]] = None          # (min, max) KTX+shuttle
    note: str = ""
    source_hint: str = ""  # short provenance note (in-app)

def badge(text: str) -> str:
    return f"<span class='badge'>{text}</span>"

def badges(items: List[str]) -> str:
    return "".join([badge(x) for x in items])

def fmt_range(r: Optional[Tuple[int,int]]) -> str:
    if not r:
        return "—"
    a,b = r
    if a == b:
        return f"{a}분"
    return f"{a}–{b}분"

def naver_directions_link(origin: str, destination: str) -> str:
    # Naver Map web directions
    # Note: Naver may ask user to confirm in browser/app.
    base = "https://map.naver.com/p/directions/"
    # Naver directions can accept query via path; but simplest is a search link.
    # We'll use place search link which user can then press '길찾기'.
    q = quote(destination)
    return f"https://map.naver.com/p/search/{q}"

# =========================
# Data (curated for "≈3h from Seoul")
# =========================
ORIGIN_DEFAULT = "서울 성동구 옥수동"

resorts: List[Resort] = [
    Resort(
        name="곤지암리조트 스키장 🏂",
        region="경기 광주",
        highlights=["수도권 최접근", "야간/심야", "초중급 친화"],
        car_min=(50, 80),  # 약 1시간 내외 (교통 따라)
        public_min=(70, 110),  # 버스+연계
        note="주말/퇴근시간 정체 시 증가",
        source_hint="자가용 약 1시간(평균) 언급 자료 기반"
    ),
    Resort(
        name="지산 포레스트 리조트 🎿",
        region="경기 이천",
        highlights=["서울 근교", "초보자 비중", "당일치기"],
        car_min=(55, 90),
        public_min=(90, 140),
        note="정체 영향 큼",
        source_hint="서울에서 약 1시간권으로 소개되는 자료 기반"
    ),
    Resort(
        name="엘리시안 강촌 ❄️",
        region="강원 춘천",
        highlights=["수도권 당일", "셔틀/철도 연계 편함", "가성비"],
        car_min=(80, 130),
        public_min=(90, 150),
        note="주말 서울→춘천 구간 정체에 민감",
        source_hint="서울에서 약 1시간30분권으로 소개되는 자료 기반"
    ),
    Resort(
        name="비발디파크 스키월드 🌙",
        region="강원 홍천",
        highlights=["슬로프 다양", "야간/새벽 운영(시즌 정책 변동)", "숙박/부대시설"],
        car_min=(90, 140),
        public_min=(100, 160),  # 셔틀/버스
        note="성수기 주말 체감 시간 증가",
        source_hint="셔틀 약 1시간40분~2시간 언급 자료 기반"
    ),
    Resort(
        name="오크밸리 스키장 🌲",
        region="강원 원주",
        highlights=["초중급 친화", "조용한 분위기", "가족형"],
        car_min=(80, 110),
        public_min=(110, 170),
        note="동서울권 출발 시 체감 접근성 좋음",
        source_hint="서울에서 약 90분권으로 소개되는 자료 기반"
    ),
    Resort(
        name="모나 용평 리조트 🏔️",
        region="강원 평창",
        highlights=["대형 리조트", "슬로프 다양", "국내 대표급"],
        car_min=(135, 165),
        public_min=(160, 200),
        ktx_min=(110, 150),  # 서울→진부(KTX)+이동(가정)
        note="폭설/동절기 고속도로 상황에 따라 변동",
        source_hint="서울→용평 운전 약 2시간21분(자료) 기반"
    ),
    Resort(
        name="휘닉스 파크(휘닉스 평창) 🐦",
        region="강원 평창",
        highlights=["슬로프/파크", "리조트형", "KTX 연계"],
        car_min=(140, 180),
        ktx_min=(110, 150),  # 서울→KTX 약 1시간30분 + 셔틀 약 20분(언급 기반)
        note="KTX 이용 시 체감이 좋아짐",
        source_hint="KTX 약 1시간30분 + 셔틀 약 20분 언급 자료 기반"
    ),
]

# =========================
# UI
# =========================
st.markdown(
    """
<div class="hero">
  <h1>⛷️ 옥수동에서 3시간 이내 스키장 리스트 ❄️✨</h1>
  <p>
    📍 출발지: <b>서울 성동구 옥수동</b> (기본값) <br/>
    ⏱️ 소요시간은 교통·날씨·시간대에 따라 변동되며, 앱은 “대략적인 비교용”입니다.
  </p>
</div>
""",
    unsafe_allow_html=True
)

st.write("")

left, right = st.columns([0.35, 0.65], gap="large")

with left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title grad-text'>🧭 필터</div>", unsafe_allow_html=True)

    origin = st.text_input("출발지(수정 가능) 📌", value=ORIGIN_DEFAULT)

    mode = st.selectbox(
        "이동수단 🚗🚌🚄",
        ["자가용(운전)", "대중교통(버스/지하철)", "KTX/철도 연계"],
        index=0
    )

    max_minutes = st.slider("최대 소요시간(분) ⏱️", min_value=60, max_value=240, value=180, step=10)

    show_sources = st.checkbox("데이터 근거(간단 힌트) 보기 🔎", value=False)

    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='note'>💡 팁: 주말 오전 출발/귀가 시간대는 정체가 심해 ‘상한(최대)’ 기준으로 보는 게 안전합니다.</div>",
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

def get_range_by_mode(r: Resort, mode: str) -> Optional[Tuple[int,int]]:
    if mode.startswith("자가용"):
        return r.car_min
    if mode.startswith("대중교통"):
        return r.public_min
    return r.ktx_min

filtered = []
for r in resorts:
    rng = get_range_by_mode(r, mode)
    if not rng:
        continue
    # Filter by upper bound (conservative)
    if rng[1] <= max_minutes:
        filtered.append((rng, r))

# Sort by upper bound then lower bound
filtered.sort(key=lambda x: (x[0][1], x[0][0], x[1].name))

with right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title grad-text'>📋 결과</div>", unsafe_allow_html=True)

    if not filtered:
        st.info("선택한 이동수단/시간 기준으로는 해당 범위에 들어오는 스키장이 없습니다. 최대 시간을 늘리거나 이동수단을 바꿔보세요.")
    else:
        st.markdown(f"✅ **{mode} 기준 {max_minutes}분 이내:** **{len(filtered)}곳**")
        st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

        for rng, r in filtered:
            mins = fmt_range(rng)
            link = naver_directions_link(origin, r.name.replace(" 🏂","").replace(" 🎿","").replace(" ❄️","").replace(" 🌙","").replace(" 🌲","").replace(" 🏔️","").replace(" 🐦",""))
            st.markdown(
                f"""
<div style="border:1px solid rgba(15,23,42,0.10); border-radius:16px; padding:14px; background:rgba(255,255,255,0.97);
            box-shadow: 0 10px 26px rgba(2,6,23,0.06); margin-bottom:12px;">
  <div style="font-weight:900; font-size:16px;">
    {r.name} <span style="font-weight:800; color:#0B63F6;">⏱️ {mins}</span>
  </div>
  <div style="margin-top:6px;">
    {badges([f"📍 {r.region}"] + [f"✨ {h}" for h in r.highlights])}
  </div>
  <div style="margin-top:8px; color: rgba(16,24,40,0.72); font-size:13px; line-height:1.5;">
    📝 {r.note if r.note else "—"}
  </div>
  <div style="margin-top:10px; font-size:13px;">
    🗺️ <a href="{link}" target="_blank" style="font-weight:900; color:#0B63F6; text-decoration:none;">네이버지도에서 검색/길찾기</a>
  </div>
</div>
""",
                unsafe_allow_html=True
            )
            if show_sources and r.source_hint:
                st.caption(f"🔎 근거 힌트: {r.source_hint}")

    st.markdown("</div>", unsafe_allow_html=True)

st.write("")
st.markdown(
    "<div class='note' style='text-align:center;'>❄️ Tip: 실제 출발 전에는 지도앱(실시간 교통)으로 최종 확인하세요.</div>",
    unsafe_allow_html=True
)
