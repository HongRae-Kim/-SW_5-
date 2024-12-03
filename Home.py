import streamlit as st

def main():
    st.title("여행 가이드 챗봇")
    st.write("챗봇 소개를 위한 페이지입니다.")

    if st.button("메인 페이지로 돌아가기"):
        st.session_state.page = "ChatBotApp"

if __name__ == "__main__":
    main()