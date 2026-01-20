import streamlit as st
from dataclasses import dataclass
from typing import List, Optional, Tuple, Dict
from urllib.parse import quote

# =========================
# Page
# =========================
st.set_page_config(
    page_title="⛷️ 옥수동 3시간 이내 스키장 + 난이도/슬로프맵",
    page_icon="❄️",
    layout="wide",
)

# =========================
# Styling (white + blue, but still pretty)
# =========================
CSS = """
<style>
.stApp { background:#ffffff; color:#101828; }
html, body, [class*="css"]{
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, "Noto Sans KR",
               "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
}
.hero{
  border-radius: 18px;
  padding: 18px 20px;
  background:
    radial-gradient(circle at 12% 20%, rgba(255, 88, 174, 0.22), transparent 40%),
    radial-gradient(circle at 88% 20%, rgba(0, 209, 255, 0.20), transparent 42%),
    radial-gradient(circle at 30% 90%, rgba(0, 255, 187, 0.14), transparent 45%),
    linear-gradient(90deg, #0B63F6 0%, #2EA8FF 55%, #7C3AED 100%);
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
  background: linear-gradient(90deg, #0B63F6, #2EA8FF, #7C3AED);
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
  background: linear-gradient(90deg, transparent, rgba(11,99,246,0.25), rgba(124,58,237,0.22), transparent);
}
.note{
  color: rgba(16,24,40,0.72);
  font-size: 13px;
  line-height: 1.55;
}
.small{
  color: rgba(16,24,40,0.62);
  font-size: 12.5px;
  line-height: 1.5;
}
div.stButton > button{
  background: linear-gradient(90deg, #0B63F6 0%, #2EA8FF 45%, #7C3AED 100%);
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
# Models
# =========================
@dataclass
class Resort:
    name: str
    region: str
    highlights: List[str]
    car_min: Optional[Tuple[int, int]] = None
    public_min: Optional[Tuple[int, int]] = None
    ktx_min: Optional[Tuple[int, int]] = None
    note: str = ""

    # Difficulty profile: values are percentages 0-100; can be None if unknown
    beginner: Optional[int] = None
    intermediate: Optional[int] = None
    advanced: Optional[int] = None
    difficulty_note: str = ""

    # Slope map resources
    slope_map_page: Optional[str] = None   # official page
    slope_map_pdf: Optional[str] = None    # official pdf
    slope_map_image: Optional[str] = None  # direct image if available

def badge(text: str) -> str:
    return f"<span class='badge'>{text}</span>"

def badges(items: List[str]) -> str:
    return "".join([badge(x) for x in items])

def fmt_range(r: Optional[Tuple[int,int]]) -> str:
    if not r:
        return "—"
    a,b = r
    return f"{a}–{b}분" if a != b else f"{a}분"

def naver_search_link(query: str) -> str:
    return f"https://map.naver.com/p/search/{quote(query)}"

def naver_directions_hint(origin: str, destination: str) -> str:
    # 네이버지도는 검색 후 '길찾기'로 연결하는 UX가 가장 안정적
    return naver_search_link(destination)

def get_range_by_mode(r: Resort, mode: str) -> Optional[Tuple[int,int]]:
    if mode.startswith("자가용"):
        return r.car_min
    if mode.startswith("대중교통"):
        return r.public_min
    return r.ktx_min

def within_minutes(rng: Optional[Tuple[int,int]], max_minutes: int) -> bool:
    if not rng:
        return False
    # 보수적으로 상한(최대) 기준
    return rng[1] <= max_minutes

def difficulty_bucket(r: Resort) -> str:
    # 사용자가 빠르게 이해할 수 있도록 “성향”을 라벨로
    if r.beginner is None or r.intermediate is None or r.advanced is None:
        return "정보 제한(정성 요약)"
    b,i,a = r.beginner, r.intermediate, r.advanced
    if b >= 50:
        return "초급 친화 🟢"
    if a >= 35:
        return "상급 비중 ↑ 🔥"
    if i >= 45:
        return "중급 중심 🟦"
    return "균형형 ⚖️"

# =========================
# Resorts (3h-ish from Oksu)
# Notes:
# - 일부 리조트는 공식 페이지 접근 제한/타임아웃 가능성이 있어, 맵은 '공식 링크' 중심으로 제공
# =========================
ORIGIN_DEFAULT = "서울 성동구 옥수동"

resorts: List[Resort] = [
    Resort(
        name="곤지암리조트 스키장 🏂",
        region="경기 광주",
        highlights=["수도권 최접근", "초·중급 다양", "당일치기 강력"],
        car_min=(50, 80),
        public_min=(70, 110),
        note="주말/퇴근 정체 시 체감시간↑",
        # Konjiam: 공식 슬로프 표에 초급/초중급/중급/중상급/상급 구성 (정량화: 초급+초중급=초급비중, 중급+중상급=중급, 상급=상급)
        beginner=33, intermediate=44, advanced=23,
        difficulty_note="공식 슬로프 표(수준 분류) 기반으로 대략 비율화(초급+초중급 / 중급+중상급 / 상급).",
        slope_map_page="https://m.konjiamresort.co.kr/ski/skiLift.dev",
        slope_map_image="https://m.konjiamresort.co.kr/common/images/ski/img-slope-keyvisual.jpg",
    ),
    Resort(
        name="지산 포레스트 리조트 🎿",
        region="경기 이천",
        highlights=["서울 근교", "초급~상급", "당일치기"],
        car_min=(55, 90),
        public_min=(90, 140),
        note="정체 영향 큼(특히 주말 오전/야간 귀가)",
        # VisitKorea에 경사/슬로프수 소개는 있으나 '난이도별 수'가 명시적으로 정리돼 있지 않아 정성 요약
        beginner=None, intermediate=None, advanced=None,
        difficulty_note="공공 관광정보에 ‘10면/경사 7~30도’ 등 스펙은 확인되나 난이도별 비율은 공식 표로 재확인이 필요.",
        slope_map_page="https://korean.visitkorea.or.kr/detail/ms_detail.do?cotid=1abed7cc-ef27-4004-9b63-474a5d1dd6ec",
    ),
    Resort(
        name="엘리시안 강촌 ❄️",
        region="강원 춘천",
        highlights=["수도권 당일", "초급~최상급", "철도/셔틀 연계"],
        car_min=(80, 130),
        public_min=(90, 150),
        note="서울→춘천 구간 정체 민감",
        beginner=None, intermediate=None, advanced=None,
        difficulty_note="공식 소개에 ‘초급부터 최상급까지’ 안내(비율은 공식 맵/슬로프 현황에서 확인 권장).",
        slope_map_page="https://www.elysian.co.kr/about-gangchon/sky",
    ),
    Resort(
        name="비발디파크 스키월드 🌙",
        region="강원 홍천",
        highlights=["슬로프 다양", "야간 운영(시즌 정책 변동)", "리조트형"],
        car_min=(90, 140),
        public_min=(100, 160),
        note="성수기/주말 상한 기준으로 보는 것이 안전",
        beginner=None, intermediate=None, advanced=None,
        difficulty_note="가이드맵(조감도/시설 지도) 제공. 난이도 비율은 운영/슬로프 안내 페이지에서 보강 가능.",
        slope_map_page="https://www.sonohotelsresorts.com/skiboard/guidemap",
        # 가이드맵 이미지가 API 형태로 내려오는 구조라 환경에 따라 로딩이 안 될 수 있어 '페이지 링크'를 기본으로 제공
    ),
    Resort(
        name="오크밸리 스키장 🌲",
        region="강원 원주",
        highlights=["가족형", "초급 친화", "규모는 소형"],
        car_min=(80, 110),
        public_min=(110, 170),
        note="총 슬로프 수가 많지 않아 ‘가볍게’ 즐기기 좋음",
        # 공식 소개에 총 3면 + 초급자용 I 코스 등(초급 친화로 정성 라벨)
        beginner=67, intermediate=33, advanced=0,
        difficulty_note="공식 소개(총 3면, 초급자 코스 명시) 기반으로 ‘초급 친화’로 단순화.",
        slope_map_page="https://oakvalley.co.kr/ski/introduction/slope",
    ),
    Resort(
        name="모나 용평 리조트 🏔️",
        region="강원 평창",
        highlights=["대형", "상급/최상급 포함", "코스 다양"],
        car_min=(135, 165),
        public_min=(160, 200),
        ktx_min=(110, 150),
        note="동절기 기상/노면/정체에 따라 편차 큼",
        # 용평은 난이도 레벨이 폭넓고 상급/최상급 코스도 다수. 정확 비율은 시즌별 오픈현황/슬로프 분류로 재집계 필요 → 여기선 정성 + 라벨
        beginner=None, intermediate=None, advanced=None,
        difficulty_note="공식 슬로프맵/오픈현황에서 초급~최상급까지 폭넓게 운영됨을 확인 가능(비율은 시즌별로 변동).",
        slope_map_page="https://www.yongpyong.co.kr/kor/skiNboard/slope/slopeMap.do",
        slope_map_pdf="https://www.yongpyong.co.kr/upload/kor/%EC%8A%AC%EB%A1%9C%ED%94%84%EB%A7%B5.pdf",
    ),
    Resort(
        name="휘닉스 파크(휘닉스 평창) 🐦",
        region="강원 평창",
        highlights=["올림픽급 파크/코스", "리조트형", "철도 연계"],
        car_min=(140, 180),
        ktx_min=(110, 150),
        note="KTX 연계 시 체감 시간 개선 가능",
        beginner=None, intermediate=None, advanced=None,
        difficulty_note="공식 안내에 ‘총 18면’ 등 규모/특성 명시(난이도별 비율은 공식 맵에서 확인 권장).",
        slope_map_page="https://phoenixhnr.co.kr/static/pyeongchang/snowpark/slope-lift",
    ),
]

# =========================
# Hero
# =========================
st.markdown(
    f"""
<div class="hero">
  <h1>⛷️ 옥수동 → 3시간 이내 스키장 ❄️ + 난이도/슬로프맵</h1>
  <p>
    📍 출발지: <b>{ORIGIN_DEFAULT}</b> (기본) · ⏱️ 소요시간은 교통/날씨/시간대에 따라 변동됩니다.<br/>
    🗺️ 슬로프맵은 ‘공식 페이지/공식 PDF’를 우선 연결하며, 가능하면 이미지 프리뷰도 제공합니다.
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

    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

    diff_pref = st.multiselect(
        "선호 난이도 성향(선택) 🎯",
        ["초급 친화 🟢", "중급 중심 🟦", "상급 비중 ↑ 🔥", "균형형 ⚖️", "정보 제한(정성 요약)"],
        default=["초급 친화 🟢", "중급 중심 🟦", "상급 비중 ↑ 🔥", "균형형 ⚖️", "정보 제한(정성 요약)"]
    )

    show_map_preview = st.checkbox("슬로프맵 미리보기(가능한 경우) 👀", value=True)
    show_notes = st.checkbox("난이도/맵 근거 메모 보기 📝", value=False)

    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='note'>💡 팁: 주말에는 ‘상한(최대 소요시간)’ 기준으로 보는 것이 안전합니다.</div>",
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# Filtering
# =========================
candidates = []
for r in resorts:
    rng = get_range_by_mode(r, mode)
    if not within_minutes(rng, max_minutes):
        continue
    bucket = difficulty_bucket(r)
    if bucket not in diff_pref:
        continue
    candidates.append((rng, r, bucket))

candidates.sort(key=lambda x: (x[0][1], x[0][0], x[1].name))

# =========================
# Rendering
# =========================
with right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title grad-text'>📋 결과</div>", unsafe_allow_html=True)

    if not candidates:
        st.info("조건에 맞는 스키장이 없습니다. 최대 소요시간을 늘리거나 난이도 필터를 조정해보세요.")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"✅ **{mode} 기준 {max_minutes}분 이내:** **{len(candidates)}곳**")
        st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

        for rng, r, bucket in candidates:
            mins = fmt_range(rng)
            map_link = r.slope_map_page or naver_search_link(r.name)
            nav_link = naver_directions_hint(origin, r.name.replace(" 🏂","").replace(" 🎿","").replace(" ❄️","").replace(" 🌙","").replace(" 🌲","").replace(" 🏔️","").replace(" 🐦",""))

            st.markdown(
                f"""
<div style="border:1px solid rgba(15,23,42,0.10); border-radius:16px; padding:14px; background:rgba(255,255,255,0.97);
            box-shadow: 0 10px 26px rgba(2,6,23,0.06); margin-bottom:12px;">
  <div style="font-weight:900; font-size:16px;">
    {r.name} <span style="font-weight:900; color:#0B63F6;">⏱️ {mins}</span>
  </div>
  <div style="margin-top:6px;">
    {badges([f"📍 {r.region}", f"🎯 {bucket}"] + [f"✨ {h}" for h in r.highlights])}
  </div>
  <div style="margin-top:8px; color: rgba(16,24,40,0.72); font-size:13px; line-height:1.5;">
    📝 {r.note if r.note else "—"}
  </div>
  <div style="margin-top:10px; font-size:13px;">
    🗺️ <a href="{nav_link}" target="_blank" style="font-weight:900; color:#0B63F6; text-decoration:none;">네이버지도에서 검색/길찾기</a>
    &nbsp;|&nbsp;
    🧭 <a href="{map_link}" target="_blank" style="font-weight:900; color:#7C3AED; text-decoration:none;">슬로프맵/슬로프 안내(공식 링크)</a>
    {f"&nbsp;|&nbsp;📄 <a href='{r.slope_map_pdf}' target='_blank' style='font-weight:900; color:#0B63F6; text-decoration:none;'>슬로프맵 PDF</a>" if r.slope_map_pdf else ""}
  </div>
</div>
""",
                unsafe_allow_html=True
            )

            # Difficulty bars (if numeric available)
            if r.beginner is not None and r.intermediate is not None and r.advanced is not None:
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.caption("🟢 초급")
                    st.progress(r.beginner / 100)
                    st.write(f"**{r.beginner}%**")
                with c2:
                    st.caption("🟦 중급")
                    st.progress(r.intermediate / 100)
                    st.write(f"**{r.intermediate}%**")
                with c3:
                    st.caption("🔥 상급")
                    st.progress(r.advanced / 100)
                    st.write(f"**{r.advanced}%**")
            else:
                st.caption("🎚️ 난이도 비율은 공식 슬로프 현황/맵에서 확인 권장(앱은 정성 요약 제공).")

            # Slope map preview (best-effort)
            if show_map_preview:
                if r.slope_map_image:
                    try:
                        st.image(r.slope_map_image, caption="🗺️ 슬로프맵(이미지 프리뷰)", use_container_width=True)
                    except Exception:
                        st.caption("⚠️ 이 환경에서는 이미지 프리뷰를 불러오지 못했습니다. 상단 ‘공식 링크’를 이용해 주세요.")
                elif r.slope_map_pdf:
                    st.caption("📄 슬로프맵이 PDF로 제공됩니다. 상단 PDF 링크로 열어보세요.")
                else:
                    st.caption("🧭 슬로프맵은 상단 ‘공식 링크’에서 확인해 주세요.")

            if show_notes and (r.difficulty_note or r.slope_map_page):
                st.markdown(f"<div class='small'>📝 메모: {r.difficulty_note if r.difficulty_note else '—'}</div>", unsafe_allow_html=True)

            st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

st.write("")
st.markdown(
    "<div class='note' style='text-align:center;'>❄️ 실제 출발 전에는 실시간 교통(지도앱 ETA)으로 최종 확인을 권장합니다.</div>",
    unsafe_allow_html=True
)
