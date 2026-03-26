import os
import base64
import streamlit as st

st.set_page_config(
    page_title="AI 업무자동화 솔루션",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# 기본 스타일
# -----------------------------
st.markdown("""
<style>
/* 전체 앱 여백 */
.block-container {
    padding-top: 2.2rem;
    padding-bottom: 1rem;
    padding-left: 1rem;
    padding-right: 1rem;
    max-width: 100%;
}

/* 상단 헤더가 너무 붙지 않도록 추가 보정 */
header[data-testid="stHeader"] {
    height: auto;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: #ffffff;
}

/* 홈 상단 제목 영역 */
.top-hero {
    padding-top: 0.5rem;
    padding-bottom: 0.8rem;
}

.main-title {
    font-size: 2rem;
    font-weight: 800;
    margin-top: 0;
    margin-bottom: 0.35rem;
    line-height: 1.35;
    word-break: keep-all;
}

.sub-title {
    font-size: 1rem;
    color: #666666;
    margin-top: 0;
    margin-bottom: 0;
    line-height: 1.6;
    word-break: keep-all;
}

/* 카드 */
.card-wrap {
    border: 1px solid #eaeaea;
    border-radius: 20px;
    padding: 14px;
    background: #ffffff;
    box-shadow: 0 4px 14px rgba(0,0,0,0.06);
    margin-bottom: 1rem;
}

.card-title {
    font-size: 1.05rem;
    font-weight: 700;
    margin-top: 0.7rem;
    margin-bottom: 0.5rem;
    line-height: 1.45;
    min-height: 3em;
    word-break: keep-all;
}

/* 상세 제목 */
.viewer-title-wrap {
    padding-top: 0.2rem;
    padding-bottom: 0.4rem;
}

.viewer-title {
    font-size: 1.4rem;
    font-weight: 800;
    margin-top: 0;
    margin-bottom: 0;
    text-align: center;
    line-height: 1.4;
    word-break: keep-all;
}

.page-indicator {
    text-align: center;
    font-size: 1rem;
    font-weight: 600;
    color: #444;
    margin-top: 0.6rem;
    margin-bottom: 0.6rem;
}

/* 슬라이드 표시 프레임 */
.slide-frame {
    width: 100%;
    height: 78vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f7f7f7;
    border-radius: 18px;
    overflow: hidden;
    border: 1px solid #ececec;
}

.slide-frame img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    display: block;
    background: white;
}

div[data-testid="stHorizontalBlock"] > div {
    width: 100%;
}

.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 3rem;
    font-weight: 700;
}

/* 모바일 대응 */
@media (max-width: 768px) {
    .block-container {
        padding-top: 2.6rem;
        padding-left: 0.6rem;
        padding-right: 0.6rem;
        padding-bottom: 0.8rem;
    }

    .top-hero {
        padding-top: 0.2rem;
        padding-bottom: 0.8rem;
    }

    .main-title {
        font-size: 1.55rem;
        line-height: 1.45;
        margin-bottom: 0.45rem;
    }

    .sub-title {
        font-size: 0.95rem;
        line-height: 1.6;
    }

    .viewer-title-wrap {
        padding-top: 0.1rem;
        padding-bottom: 0.45rem;
    }

    .viewer-title {
        font-size: 1.12rem;
        line-height: 1.45;
        padding-left: 0.2rem;
        padding-right: 0.2rem;
    }

    .slide-frame {
        height: 70vh;
        border-radius: 14px;
    }

    .card-title {
        font-size: 0.98rem;
    }

    .stButton > button {
        height: 2.8rem;
        font-size: 0.95rem;
    }
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 프로젝트 정의
# -----------------------------
projects = {
    "sol1": "근무시간 및 수당 자동 계산 시스템",
    "sol2": "OCR 기반 이미지 데이터 변환",
    "sol3": "중복 자산 탐색 자동화",
    "sol4": "뉴스 크롤링 및 콘텐츠 자동 생성",
    "sol5": "VoC 감정 분석 웹앱",
    "sol6": "데이터 전처리 자동화",
}

# -----------------------------
# 상태 관리
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "project" not in st.session_state:
    st.session_state.project = None

if "idx" not in st.session_state:
    st.session_state.idx = 0

# -----------------------------
# 유틸 함수
# -----------------------------
def load_images(folder: str):
    if not os.path.exists(folder):
        return []

    valid_ext = (".png", ".jpg", ".jpeg", ".webp")
    files = [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith(valid_ext)
    ]
    return sorted(files)

def image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def render_big_image(image_path: str):
    ext = os.path.splitext(image_path)[1].lower()
    mime = "image/png"
    if ext in [".jpg", ".jpeg"]:
        mime = "image/jpeg"
    elif ext == ".webp":
        mime = "image/webp"

    img_b64 = image_to_base64(image_path)
    st.markdown(
        f"""
        <div class="slide-frame">
            <img src="data:{mime};base64,{img_b64}" alt="slide">
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# 홈 화면
# -----------------------------
def show_home():
    st.markdown("""
    <div class="top-hero">
        <div class="main-title">AI 업무자동화 솔루션</div>
        <div class="sub-title">프로젝트를 선택하면 슬라이드를 한 장씩 크게 볼 수 있습니다.</div>
    </div>
    """, unsafe_allow_html=True)

    keys = list(projects.keys())

    for row_start in range(0, len(keys), 2):
        cols = st.columns(2, gap="medium")
        row_keys = keys[row_start:row_start + 2]

        for col, key in zip(cols, row_keys):
            title = projects[key]
            folder = os.path.join("slides", key)
            images = load_images(folder)
            thumbnail = images[0] if images else None

            with col:
                st.markdown('<div class="card-wrap">', unsafe_allow_html=True)

                if thumbnail:
                    st.image(thumbnail, use_container_width=True)

                st.markdown(f'<div class="card-title">{title}</div>', unsafe_allow_html=True)

                if st.button("프로젝트 보기", key=f"open_{key}"):
                    st.session_state.page = "detail"
                    st.session_state.project = key
                    st.session_state.idx = 0
                    st.rerun()

                st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# 상세 화면
# -----------------------------
def show_detail():
    key = st.session_state.project
    title = projects[key]

    folder = os.path.join("slides", key)
    images = load_images(folder)

    if not images:
        st.error("해당 프로젝트 폴더에 이미지가 없습니다.")
        if st.button("홈으로 돌아가기"):
            st.session_state.page = "home"
            st.rerun()
        return

    if st.session_state.idx < 0:
        st.session_state.idx = 0
    if st.session_state.idx >= len(images):
        st.session_state.idx = len(images) - 1

    top1, top2, top3 = st.columns([1, 4, 1])

    with top1:
        if st.button("← 홈", key="go_home"):
            st.session_state.page = "home"
            st.rerun()

    with top2:
        st.markdown(
            f"""
            <div class="viewer-title-wrap">
                <div class="viewer-title">{title}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with top3:
        st.empty()

    render_big_image(images[st.session_state.idx])

    st.markdown(
        f'<div class="page-indicator">{st.session_state.idx + 1} / {len(images)}</div>',
        unsafe_allow_html=True
    )

    nav1, nav2, nav3 = st.columns([1.2, 1, 1.2], gap="small")

    with nav1:
        prev_disabled = st.session_state.idx == 0
        if st.button("◀ 이전", disabled=prev_disabled, key="prev_btn"):
            st.session_state.idx -= 1
            st.rerun()

    with nav2:
        current = st.selectbox(
            "슬라이드 이동",
            options=list(range(len(images))),
            index=st.session_state.idx,
            format_func=lambda x: f"{x + 1}번 슬라이드",
            label_visibility="collapsed"
        )
        if current != st.session_state.idx:
            st.session_state.idx = current
            st.rerun()

    with nav3:
        next_disabled = st.session_state.idx == len(images) - 1
        if st.button("다음 ▶", disabled=next_disabled, key="next_btn"):
            st.session_state.idx += 1
            st.rerun()

# -----------------------------
# 라우팅
# -----------------------------
if st.session_state.page == "home":
    show_home()
else:
    show_detail()
