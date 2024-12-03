import streamlit as st

if "page" not in st.session_state:
    st.session_state.page = "Home"

def navigate_to(page_name):
    st.session_state.page = page_name

if st.session_state.page == "Home":
    import Home
    Home.main()
elif st.session_state.page == "ChatBotApp":
    import ChatBotApp
    ChatBotApp.main()
