import streamlit as st
from urllib.parse import quote
import ollama

# 모델 이름 저장, Ollama 로컬 서버 실행되고 있어야 함
model_name = "hf.co/MLP-KTLim/llama-3-Korean-Bllossom-8B-gguf-Q4_K_M"

# Kakao 지도 API를 사용하여 HTML iframe 생성
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

# 상황별 프롬프트 설정 로직
def generate_prompt(user_input):
    if "춘천 식당" in user_input:
        prompt = f'''
        당신은 춘천 여행 가이드에 대한 정보를 사용자에게 소개해야합니다.
        춘천의 유명한 맛집 중, 추천하는 식사 장소들을 위치와 추천 메뉴와 함께 안내해주세요.

        1. 맛집 이름: 방문할 장소의 이름을 기재합니다.
        2. 위치: 장소를 방문할 적절한 시간을 제시합니다.
        3. 가격대: 해당 식당의 가격대를 간단하게 설명해주세요.

        사용자가 요청한 내용: "{user_input}"
        '''
    elif "춘천 관광지" in user_input:
        prompt = f'''
        당신은 춘천 여행 가이드에 대한 정보를 사용자에게 소개해야합니다.
        춘천의 주요 관광지들을 시간 계획과 함께 안내하고, 각 장소의 흥미로운 점도 설명해주세요.

        1. 관광지 이름: 방문할 장소의 이름을 기재합니다.
        2. 위치: 장소를 방문할 적절한 시간을 제시합니다.
        3. 가격대: 해당 관광지의 가격대를 간단하게 설명해주세요.

        사용자가 요청한 내용: "{user_input}"
        '''
    elif "춘천 숙소" in user_input:
        prompt = f'''
        당신은 춘천 여행 가이드에 대한 정보를 사용자에게 소개해야합니다.
        춘천의 인기 숙소들을 가격대와 위치를 고려하여 추천해주세요.

        1. 숙소 이름: 방문할 숙소의 이름을 기재합니다.
        2. 위치: 숙소가 위치한 적절한 시간을 제시합니다.
        3. 가격대: 해당 숙소의 가격대를 간단하게 설명해주세요.

        사용자가 요청한 내용: "{user_input}"
        '''
    else:
        # 올바르지 않은 입력 처리
        return None  # None을 반환하여 후속 처리에서 확인 가능하게 함
    return prompt

# Streamlit 앱 구현
def main():
    # 화면 너비 설정
    st.set_page_config(layout="wide")

    # 앱 제목 및 설명
    st.title("🗺️ 여행 가이드 챗봇")
    st.write("검색하고자 하는 장소를 입력하세요. 현재는 **춘천 지역**만 지원합니다.")

    # 사용자 입력
    user_input = st.text_input("검색할 장소를 입력하세요:", placeholder="예: 춘천 식당, 춘천 관광지 ...")

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

    with col2:
        st.subheader("📅 추천 일정")
        st.write("chatBot으로 일정 출력하기")
        if user_input.strip():
            response_placeholder = st.empty()
            try:
                # 상황별 프롬프트 생성
                prompt = generate_prompt(user_input)
                
                if prompt:
                    response_stream = ollama.chat(
                        model=model_name,
                        messages=[
                            {
                                "role": "user",
                                "content": prompt,
                            },
                        ],
                        stream=True  # 실시간 출력
                    )

                    full_response = ""
                    MAX_DISPLAY_LENGTH = 700  # 응답 최대 길이 제한

                    for chunk in response_stream:
                        # 실시간으로 응답을 추가
                        full_response += chunk['message']['content']
                        
                        # 응답이 너무 길 경우 표시할 부분만 자르고 스트리밍 중단
                        if len(full_response) > MAX_DISPLAY_LENGTH:
                            full_response = full_response[:MAX_DISPLAY_LENGTH] + "..."
                            response_placeholder.markdown(full_response)  # 실시간 응답 출력
                            st.warning("⚠️ 응답이 너무 길어 일부가 잘렸습니다.")
                            break
                        else:
                            response_placeholder.markdown(full_response)  # 실시간 응답 업데이트
                    
                    st.success("응답 완료")

            except Exception as e:
                st.error(f"오류 발생: {e}")
            
# 메인 실행
if __name__ == "__main__":
    main()