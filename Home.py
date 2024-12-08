import streamlit as st

def add_bg_from_url(image_url, background_color="#b7c1c6"):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-attachment: fixed;
            background-size: contain; /* 이미지 잘리지 않도록 설정 */
            background-position: center; /* 이미지 중앙 정렬 */
            background-repeat: no-repeat; /* 이미지 반복 금지 */
            background-color: {background_color}; /* 여백 색상 설정 */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# 배경 이미지와 여백 색상 설정
add_bg_from_url("https://i.imgur.com/ZubPpxp.png", background_color="#b7c1c6")

def main():
    st.title("여행 가이드 챗봇")
    st.write("챗봇 소개를 위한 페이지입니다.")

    if st.button("메인 페이지로 가기"):
        st.session_state.page = "chatBotApp"
    elif st.button("소개 페이지로 가기"):
        st.session_state.page = "Subpage"

if __name__ == "__main__":
    main()
