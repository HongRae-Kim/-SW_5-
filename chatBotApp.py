import streamlit as st
from urllib.parse import quote

# Kakao 지도 API를 사용하여 HTML iframe 생성
def generate_map_iframe_html(query, width, height):
    encoded_query = quote(query)
    return f"""
    <iframe
        width="{width}"
        height="{height}"
        src="https://map.kakao.com/link/search/{encoded_query}"
        frameborder="0"
        allowfullscreen>
    </iframe>
    """

# Streamlit 앱 구현
def main():
    # 화면 너비 설정
    st.set_page_config(layout="wide")

    # 앱 제목 및 설명
    st.title("🗺️ 여행 가이드 챗봇")
    st.write("검색하고자 하는 장소를 입력하세요. 현재는 **춘천 지역**만 지원합니다.")

    # 사용자 입력
    user_input = st.text_input("검색할 장소를 입력하세요:", placeholder="예: 춘천 카페")

    # 기본 지도 HTML
    map_html = None
    if user_input:
        if "춘천" in user_input:
            query = user_input
            map_html = generate_map_iframe_html(query, "100%", "600px")
        else:
            st.warning("현재는 춘천 지역만 지원합니다. 검색어에 '춘천'을 포함해주세요.")

    # 레이아웃 설정: 사이드바, 지도, 일정
    col1, col2 = st.columns([5, 3])

    # 사이드바: 빠른 탐색 버튼
    with st.sidebar:
        st.header("🔍 빠른 탐색")
        st.write("아래 버튼을 눌러 원하는 정보를 바로 볼 수 있습니다")
        if st.button("춘천 식당"):
            query = "춘천 식당"
            map_html = generate_map_iframe_html(query, "100%", "600px")
        if st.button("춘천 관광지"):
            query = "춘천 관광지"
            map_html = generate_map_iframe_html(query, "100%", "600px")
        if st.button("춘천 숙소"):
            query = "춘천 숙소"
            map_html = generate_map_iframe_html(query, "100%", "600px")

    # 지도 출력
    with col1:
        if map_html:
            st.components.v1.html(map_html, height=600)
        else:
            st.info("검색 결과가 여기에 표시됩니다.")

    # 일정 관련 콘텐츠 출력
    with col2:
        st.subheader("📅 추천 일정")
        st.write("chatBot으로 일정 출력하기")

# 메인 실행
if __name__ == "__main__":
    main()
