import streamlit as st
from urllib.parse import quote

KAKAO_API_KEY = "Your_API_KEY"

# HTML을 렌더링하기 위한 기본 템플릿
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
    # 화면 너비 제한 해제
    st.set_page_config(layout="wide")

    st.title("여행 가이드 챗봇")
    st.write("검색하고자 하는 장소를 입력하세요.")

    user_input = st.text_input("질문을 입력하세요:")

    if user_input:
        if "춘천" in user_input:
            query = user_input
            map_html = generate_map_iframe_html(query, "100%", "600px")
            # 왼쪽에 버튼, 중간에 지도, 우측에 일정 표시
            col1, col2, col3 = st.columns([1, 5, 3])
            with col1:
                if st.button("식당"):
                    query = user_input.replace(user_input, "춘천 식당")
                    map_html = generate_map_iframe_html(query, "100%", "600px")
                if st.button("관광지"):
                    query = user_input.replace(user_input, "춘천 관광지")
                    map_html = generate_map_iframe_html(query, "100%", "600px")
                if st.button("숙소"):
                    query = user_input.replace(user_input, "춘천 숙소")
                    map_html = generate_map_iframe_html(query, "100%", "600px")
            with col2:
                st.components.v1.html(map_html, height=600)
            with col3:
                st.write("여기에 일정 챗봇으로 출력")
        else:
            st.warning("춘천 지역만 가능합니다")

if __name__ == "__main__":
    main()
