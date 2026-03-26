import streamlit as st
from pathlib import Path

# --------------------------------------------------
# 기본 경로 설정
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
SLIDES_DIR = BASE_DIR / "slides"

# 지원할 이미지 확장자
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}

# --------------------------------------------------
# 솔루션 폴더 목록 가져오기
# --------------------------------------------------
@st.cache_data
def get_solution_folders():
    """
    slides 폴더 아래의 솔루션 폴더 목록을 반환
    """
    if not SLIDES_DIR.exists():
        return []

    folders = [p for p in SLIDES_DIR.iterdir() if p.is_dir()]
    folders = sorted(folders, key=lambda x: x.name.lower())
    return [folder.name for folder in folders]


# --------------------------------------------------
# 특정 솔루션 폴더 안의 이미지 경로 수집
# --------------------------------------------------
@st.cache_data
def get_solution_image_paths(solution_name: str):
    """
    slides/solution_name 아래에서 이미지 파일을 재귀적으로 탐색하여
    정렬된 경로 리스트를 반환
    """
    solution_dir = SLIDES_DIR / solution_name

    if not solution_dir.exists() or not solution_dir.is_dir():
        return []

    image_files = [
        p for p in solution_dir.rglob("*")
        if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
    ]

    # 파일명 기준 + 전체 경로 기준 정렬
    image_files = sorted(image_files, key=lambda x: str(x).lower())

    # cache_data에서 직렬화 안정성을 위해 문자열로 반환
    return [str(p) for p in image_files]


# --------------------------------------------------
# 이미지 바이트 자체를 캐시에 저장
# --------------------------------------------------
@st.cache_data
def load_image_bytes(image_path: str):
    """
    이미지 파일을 bytes로 읽어서 cache
    """
    path = Path(image_path)
    if not path.exists():
        return None
    return path.read_bytes()


# --------------------------------------------------
# 선택된 솔루션의 모든 이미지를 미리 읽어서 캐시에 적재
# --------------------------------------------------
@st.cache_data
def preload_solution_images(solution_name: str):
    """
    특정 솔루션의 이미지들을 모두 읽어서 캐시에 적재
    반환값: [{"name": 파일명, "path": 경로, "bytes": 이미지바이트}, ...]
    """
    image_paths = get_solution_image_paths(solution_name)

    results = []
    for image_path in image_paths:
        img_bytes = load_image_bytes(image_path)
        if img_bytes is not None:
            results.append({
                "name": Path(image_path).name,
                "path": image_path,
                "bytes": img_bytes
            })

    return results


# --------------------------------------------------
# 상세 보기 화면
# --------------------------------------------------
def show_detail(selected_solution: str):
    """
    선택된 솔루션의 이미지 상세 보기
    """

    # 솔루션이 바뀌면 idx 초기화
    if "current_solution" not in st.session_state:
        st.session_state.current_solution = selected_solution

    if "idx" not in st.session_state:
        st.session_state.idx = 0

    if st.session_state.current_solution != selected_solution:
        st.session_state.current_solution = selected_solution
        st.session_state.idx = 0

    # 캐시된 이미지 불러오기
    images = preload_solution_images(selected_solution)

    st.subheader(f"솔루션 상세: {selected_solution}")

    if not images:
        st.warning(f"'{selected_solution}' 폴더에서 이미지 파일을 찾지 못했습니다.")
        return

    # 인덱스 보정
    st.session_state.idx = max(0, min(st.session_state.idx, len(images) - 1))

    current_image = images[st.session_state.idx]

    # 상단 정보
    st.write(f"총 이미지 수: {len(images)}")
    st.write(f"현재 이미지: {st.session_state.idx + 1} / {len(images)}")
    st.caption(current_image["path"])

    # 이미지 표시
    st.image(current_image["bytes"], caption=current_image["name"], use_container_width=True)

    # 이전 / 다음 버튼
    col1, col2, col3 = st.columns([1, 1, 3])

    with col1:
        if st.button("이전", use_container_width=True):
            st.session_state.idx = max(0, st.session_state.idx - 1)
            st.rerun()

    with col2:
        if st.button("다음", use_container_width=True):
            st.session_state.idx = min(len(images) - 1, st.session_state.idx + 1)
            st.rerun()

    # 썸네일 느낌의 파일명 목록
    with st.expander("이미지 목록 보기"):
        for i, img in enumerate(images):
            marker = "👉 " if i == st.session_state.idx else ""
            st.write(f"{marker}{i+1}. {img['name']}")


# --------------------------------------------------
# 메인 화면
# --------------------------------------------------
def main():
    st.title("솔루션 이미지 뷰어")

    solution_folders = get_solution_folders()

    if not solution_folders:
        st.error("slides 폴더가 없거나, 솔루션 폴더가 없습니다.")
        st.info(f"확인 경로: {SLIDES_DIR}")
        return

    selected_solution = st.selectbox("솔루션 선택", solution_folders)

    # 선택한 솔루션 외에, 첫 진입 시 일부 미리 캐시하고 싶으면 여기서 가능
    # preload_solution_images(selected_solution)

    show_detail(selected_solution)


if __name__ == "__main__":
    main()
