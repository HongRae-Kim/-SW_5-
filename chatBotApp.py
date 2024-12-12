import streamlit as st
import ollama
import re
import requests
import random
from streamlit_option_menu import option_menu
from urllib.parse import quote
from datetime import datetime, timedelta

st.set_page_config(layout="wide", page_title="여행가이드챗봇", page_icon="🗺️")

def add_bg_from_url(
    image_url, 
    background_color="#b7c1c6", 
    background_position="center", 
    background_repeat="no-repeat"
):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: {background_color} url("{image_url}");
            background-attachment: fixed;
            background-position: {background_position};
            background-repeat: {background_repeat};
            background-size: cover;
            /* 배경 이미지 위에 반투명 오버레이를 깔아 텍스트 가독성 향상 */
            background-blend-mode: overlay;
            background-color: {background_color};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

model_name = "hf.co/MLP-KTLim/llama-3-Korean-Bllossom-8B-gguf-Q4_K_M"

PUBLIC_DATA_SERVICE_KEY = "acV+BKrGo2bkYzStq90pG+G1uma95W5/awstYhpC/y2GRwoRj7Hj5ZFArwD5ZHqaaYzFtlIYNB6XC0DM6+anxA=="
KAKAO_API_KEY = "8718fcfe61913308c50d0e5974a0a68f"
OPENWEATHER_API_KEY = "ed8a40d22e5db3f3ee51b6a0dcdf6d42"

def generate_map_iframe_html(query, width, height):
    # Kakao 지도를 iframe 형태로 표시하기 위한 HTML 생성 함수
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

def get_weather_forecast(city):
    # OpenWeather API를 이용해 날씨 예보 정보를 가져오는 함수
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={OPENWEATHER_API_KEY}&units=metric&lang=kr"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        forecast_data = []
        current_time = datetime.now()

        # 현재 시간과 12시간 후 예보 정보 추출
        for delta in [0, 12]:
            forecast_time = current_time + timedelta(hours=delta)
            forecast_data.append({
                "time": forecast_time.strftime("%H시 %M분"),
                "temp": data['list'][delta]['main']['temp'],
                "description": data['list'][delta]['weather'][0]['description'],
                "weekday": forecast_time.strftime("%A"),
                "temp_min": data['list'][delta]['main']['temp_min'],
                "temp_max": data['list'][delta]['main']['temp_max'],
            })

        # 일별 최저/최고 기온 계산
        daily_min_max = {}
        for forecast in data['list']:
            date = datetime.fromtimestamp(forecast['dt']).strftime('%Y-%m-%d')
            temp_min = forecast['main']['temp_min']
            temp_max = forecast['main']['temp_max']
            if date not in daily_min_max:
                daily_min_max[date] = {'temp_min': temp_min, 'temp_max': temp_max}
            else:
                daily_min_max[date]['temp_min'] = min(daily_min_max[date]['temp_min'], temp_min)
                daily_min_max[date]['temp_max'] = max(daily_min_max[date]['temp_max'], temp_max)

        return forecast_data, daily_min_max
    else:
        return None, None

def get_restaurant_info():
    # 공공데이터포털 API에서 맛집 정보를 가져오는 함수
    base_url = "https://api.odcloud.kr/api"
    endpoint = "/15050522/v1/uddi:3e709331-acba-4c95-a69a-8845740626d6"
    url = f"{base_url}{endpoint}"
    params = {
        "page": 1,
        "perPage": 10,
        "returnType": "JSON",
        "serviceKey": PUBLIC_DATA_SERVICE_KEY 
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        response_data = response.json()
        restaurant_list = []
        for item in response_data.get("data", []):
            restaurant_info = {
                "업소명": item.get("업소명"),
                "소재지": item.get("소재지(도로명)"),
                "음식의유형": item.get("음식의유형"),
                "추천메뉴": item.get("주된음식")
            }
            restaurant_list.append(restaurant_info)
        # 최대 3개까지 랜덤 추천
        return random.sample(restaurant_list, min(3, len(restaurant_list)))
    else:
        st.error(f"API 요청에 실패했습니다: 상태 코드 {response.status_code}")
        return None

# 공공데이터포털 API에서 숙박업소 정보를 가져오는 함수
def get_accommodation_info():
    base_url = "https://api.odcloud.kr/api"
    endpoint = "/3036290/v1/uddi:2928fb68-349b-4488-b074-d545bff65072"
    url = f"{base_url}{endpoint}"
    params = {
        "page": 1,
        "perPage": 10,
        "returnType": "JSON",
        "serviceKey": PUBLIC_DATA_SERVICE_KEY  
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        response_data = response.json()
        accommodation_list = []
        for item in response_data.get("data", []):
            accommodation_info = {
                "업소명": item.get("업소명"),
                "소재지": item.get("소재지도로명주소"),
                "업태": item.get("업태"),
            }
            accommodation_list.append(accommodation_info)
        return random.sample(accommodation_list, min(3, len(accommodation_list)))
    else:
        st.error(f"API 요청에 실패했습니다: 상태 코드 {response.status_code}")
        return None

# 공공데이터포털 API에서 테마 관광지 정보를 가져오는 함수
def get_thematic_tour_info():
    base_url = "https://api.odcloud.kr/api"
    endpoint = "/15103358/v1/uddi:2c258f70-483e-40da-80f9-8103d8f9e239"
    url = f"{base_url}{endpoint}"
    params = {
        "pageNo": 1,
        "perPage": 10,
        "returnType": "JSON",
        "serviceKey": PUBLIC_DATA_SERVICE_KEY 
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        if response.status_code == 200:
            response_data = response.json()
            tour_list = []
            for item in response_data.get("data", []):
                tour_info = {
                    "테마": item.get("테마"),
                    "요약": item.get("요약"),
                    "코스정보": item.get("코스정보"),
                }
                tour_list.append(tour_info)
            selected_tours = random.sample(tour_list, min(1, len(tour_list)))
            return selected_tours
        else:
            print(f"API 요청에 실패했습니다: 상태 코드 {response.status_code}")
            return None 
        
    except requests.exceptions.RequestsDependencyWarning as err:
        print(f"API 요청 오류 발생: {err}") 
        return None

def call_model(prompt, placeholder):
    try:
        response_stream = ollama.chat(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            stream=True
        )
        full_response = ""
        for chunk in response_stream:
            if 'message' in chunk:
                full_response += chunk['message']['content']
                placeholder.markdown(full_response)
        st.success("모델 응답 완료")
    except Exception as e:
        st.error(f"모델 호출 오류가 발생했습니다: {e}")

# 모델에게 전달할 프롬프트를 생성하는 함수
def generate_prompt(restaurants=None, accommodations=None, tourist=None, weather_summary=None, map_query=None):
    api_result = ""

    if restaurants:
        api_result += "\n[맛집 정보]\n"
        for res in restaurants:
            api_result += f"업소명: {res['업소명']}, 위치: {res['소재지']}, 음식 유형: {res['음식의유형']}, 추천 메뉴: {res['추천메뉴']}\n"

        if weather_summary:
            api_result += f"\n[날씨 정보]\n{weather_summary}\n"
        if map_query:
            api_result += f"\n[지도 정보]\n해당 지역 지도 검색: {map_query}\n"

        prompt = f"""
        다음은 춘천의 인기 맛집에 대한 정보입니다. {api_result}
        위 내용을 사용하여 당신은 춘천 맛집 가이드에 대한 정보를 사용자에게 소개하세요.

        예시:
        1. 맛집 이름: 방문할 맛집을 기재.
        2. 위치: 장소 위치를 간단히 설명.
        3. 음식 유형: 음식 종류를 간단히 설명.
        4. 추천 메뉴: 추천하는 메뉴를 설명.

        날씨 정보와 지도 정보를 참고하여, 춘천의 유명한 맛집들을 위치와 추천 메뉴를 고려하여 추천해주세요.
        """
        return prompt

    elif accommodations:
        api_result += "\n[숙박업소 정보]\n"
        for acc in accommodations:
            api_result += f"업소명: {acc['업소명']}, 위치: {acc['소재지']}, 업태: {acc['업태']}\n"

        if weather_summary:
            api_result += f"\n[날씨 정보]\n{weather_summary}\n"
        if map_query:
            api_result += f"\n[지도 정보]\n해당 지역 지도 검색: {map_query}\n"

        prompt = f"""
        다음은 춘천의 인기 숙박업소에 대한 정보입니다. {api_result}
        위 내용을 사용하여 당신은 춘천 여행 가이드에서 숙박 정보를 사용자에게 소개하세요.

        예시:
        1. 숙박업소 이름: 숙박업소명 기재.
        2. 위치: 숙소 위치를 간단히 설명.
        3. 업태: 관광호텔, 여관업, 여인숙업, 일반호텔, 숙박업 기타 등 분류 기재.

        날씨 정보와 지도 정보를 참고하여, 춘천의 숙박업소들을 추천해주세요.
        """
        return prompt

    elif tourist:
        api_result += "\n[관광지 정보]\n"
        for tour in tourist:
            api_result += f"테마: {tour['테마']}, 요약: {tour['요약']}, 코스정보: {tour['코스정보']}\n"

        if weather_summary:
            api_result += f"\n[날씨 정보]\n{weather_summary}\n"
        if map_query:
            api_result += f"\n[지도 정보]\n해당 지역 지도 검색: {map_query}\n"

        prompt = f"""
        다음은 춘천의 관광지에 대한 정보입니다. {api_result}
        위 내용을 사용하여 당신은 춘천 관광 가이드에 대한 정보를 사용자에게 소개하세요.

        예시:
        1. 코스정보: 코스 개요를 간단히 설명.
        2. 소개: 코스 관련 특징을 설명.
        3. 추천: 누구와 함께 즐기면 좋을지 설명.

        날씨 정보와 지도 정보를 참고하여, 춘천의 유명한 관광지를 추천해주세요.
        """
        return prompt

    else:
        return "사용 가능한 정보가 없습니다."

def main():
    add_bg_from_url("https://i.imgur.com/5hwglBj.png", background_color="#b7c1c6")
    st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            background-color: #2C3E50;
            min-width: 200px;
            max-width: 300px;
        }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
            color: #FFFFFF;
        }
    </style>
    """,
    unsafe_allow_html=True,
    )

    st.title("🗺️ 여행 가이드 챗봇")
    st.write("검색하고자 하는 장소를 입력하세요. 현재는 **춘천 지역**만 지원합니다")

    with st.sidebar:
        st.header("🔍 빠른 탐색")
        menu = option_menu(
            menu_title="Menu",
            options=["춘천 식당", "춘천 숙소", "춘천 관광지"],
            icons=["apple", "building", "backpack"],
            default_index=0,
            styles={
                "container": {"padding": "5!important", "background-color": "#AAAAAA"},
                "icon": {"color": "white", "font-size": "25px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#CDCDFD",
                },
                "nav-link-selected": {
                    "background-color": "#2C3E50",
                },
            },
        )

        my_date = st.date_input("원하는 날짜를 선택하세요", datetime.now())

    # 사용자 입력을 받아 처리
    user_input = st.text_input("검색할 장소를 입력하세요:", placeholder="예: 춘천 식당, 춘천 관광지 ...")

    # 지도 표시를 위한 검색어 결정
    map_query = user_input if user_input else menu

    # 날씨 정보 가져오기
    forecast_data, daily_min_max = get_weather_forecast("Chuncheon")

    # 날씨 요약 문자열 생성
    weather_summary = ""
    if forecast_data:
        current_weather = forecast_data[0]
        weather_summary = f"현재시간({current_weather['time']}) 기준 온도: {current_weather['temp']}°C, 날씨: {current_weather['description']}입니다."

    restaurants, accommodations, tourist = None, None, None

    col1, col2 = st.columns([4, 6])

    with col1:
        st.subheader("📅 추천 일정")
        response_placeholder = st.empty() # 사용자 입력에 따른 추천 일정 생성 

        try:
            # 맛집 검색
            if re.search(r"(춘천).*?(식당|맛집)", user_input, re.IGNORECASE) or "식당" in menu:
                restaurants = get_restaurant_info()
                if restaurants:
                    prompt = generate_prompt(restaurants=restaurants, weather_summary=weather_summary, map_query=map_query)
                    with st.spinner("모델 응답 생성중..."):
                        call_model(prompt, response_placeholder)

            # 숙소 검색
            elif re.search(r"(춘천).*?(숙소)", user_input, re.IGNORECASE) or "숙소" in menu:
                accommodations = get_accommodation_info()
                if accommodations:
                    prompt = generate_prompt(accommodations=accommodations, weather_summary=weather_summary, map_query=map_query)
                    with st.spinner("모델 응답 생성중..."):
                        call_model(prompt, response_placeholder)

            # 관광지 검색
            elif re.search(r"(춘천).*?(관광지)", user_input, re.IGNORECASE) or "관광지" in menu:
                tourist = get_thematic_tour_info()
                if tourist:
                    prompt = generate_prompt(tourist=tourist, weather_summary=weather_summary, map_query=map_query)
                    with st.spinner("모델 응답 생성중..."):
                        call_model(prompt, response_placeholder)

        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")

    # 지도 및 날씨 정보 출력 (col2)
    with col2:
        map_html = generate_map_iframe_html(map_query, "100%", "600")
        if map_html:
            st.components.v1.html(map_html, height=600)
        else:
            st.info("지도가 여기에 표시됩니다.")

        # 날씨 정보 표시
        if forecast_data:
            st.subheader("☀️ 춘천 날씨 예보")
            for i, forecast in enumerate(forecast_data):
                left_col, right_col = st.columns([1, 1])  
                with left_col: # 현재 시간을 기준으로 시간, 온도, 날씨 출력(left_col)
                    st.write(f"🕓시간: {forecast['time']}")
                    st.write(f"🌡️온도: {forecast['temp']}°C")
                    st.write(f"☁️날씨: {forecast['description']}")
                with right_col: # 요일과 그 날 최저, 최고 기온 출력(right_col)
                    weekday_display = (my_date + timedelta(days=i)).strftime("%A")
                    st.write(f"📅요일: {weekday_display}")
                    date_key = (my_date + timedelta(days=i)).strftime('%Y-%m-%d')
                    if date_key in daily_min_max:
                        st.write(f"🌡️최저 기온: {daily_min_max[date_key]['temp_min']}°C")
                        st.write(f"🌡️최고 기온: {daily_min_max[date_key]['temp_max']}°C")
                st.write("------")
        else:
            st.error("날씨 정보를 가져올 수 없습니다.")


if __name__ == "__main__":
    main()
