import streamlit as st
from urllib.parse import quote
import requests
from datetime import datetime, timedelta

# Kakao 지도 API를 사용하여 HTML iframe 생성
KAKAO_API_KEY = "Your_API_KEY"

# OpenWeather API Key
OPENWEATHER_API_KEY = "ed8a40d22e5db3f3ee51b6a0dcdf6d42"

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

# 날씨 예보를 가져오는 함수
def get_weather_forecast(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={OPENWEATHER_API_KEY}&units=metric&lang=kr"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        forecast_data = []

        current_time = datetime.now()
        
        # 시간 구하기
        for delta in [0, 3, 6]:  # 0은 현재시간, 3은 +3시간, 6은 +6시간
            forecast_time = current_time + timedelta(hours=delta)
            forecast_data.append({
                "time": forecast_time.strftime("%H시 %M분"),  
                "temp": data['list'][delta]['main']['temp'],
                "description": data['list'][delta]['weather'][0]['description'],
                "weekday": forecast_time.strftime("%A"),  
                "temp_min": data['list'][delta]['main']['temp_min'],  
                "temp_max": data['list'][delta]['main']['temp_max'],  
            })
        
        # 각 요일별로 최저 및 최고 기온을 구하기
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

# Streamlit 앱 구현
def main():
    # 화면 너비 설정
    st.set_page_config(layout="wide")

    # 앱 제목 및 설명
    st.title("🗺️ 여행 가이드 챗봇")
    st.write("검색하고자 하는 장소를 입력하세요. 현재는 **춘천 지역**만 지원합니다.")

    # 검색어 입력
    user_input = st.text_input("검색할 장소를 입력하세요:", placeholder="예: 춘천 카페")

    # 기본 지도 HTML
    map_html = None
    if user_input:
        if "춘천" in user_input:
            query = user_input
            map_html = generate_map_iframe_html(query, "100%", "600px")
        else:
            st.warning("현재는 춘천 지역만 지원합니다. 검색어에 '춘천'을 포함해주세요.")

    # 레이아웃 설정: 지도, 날씨 예보, 추천 일정
    col1, col2 = st.columns([5, 3])

    with st.sidebar:
        st.header("🔍 빠른 탐색")
        st.write("아래 버튼을 눌러 원하는 정보를 바로 볼 수 있습니다")

        # 사이드바 버튼 클릭 후 지도 HTML 업데이트
        if st.button("춘천 식당"):
            query = "춘천 식당"
            map_html = generate_map_iframe_html(query, "100%", "600px")
        if st.button("춘천 관광지"):
            query = "춘천 관광지"
            map_html = generate_map_iframe_html(query, "100%", "600px")
        if st.button("춘천 숙소"):
            query = "춘천 숙소"
            map_html = generate_map_iframe_html(query, "100%", "600px")

    # 지도 및 날씨 정보 출력 (col1)
    with col1:
        if map_html:
            st.components.v1.html(map_html, height=600)
        else:
            st.info("검색 결과가 여기에 표시됩니다.")

        # 날씨 예보 출력
        forecast_data = None
        daily_min_max = None
        if "춘천" in user_input:
            forecast_data, daily_min_max = get_weather_forecast("Chuncheon")
            if forecast_data:
                st.subheader("☀️ 춘천 날씨 예보")
                for i, forecast in enumerate(forecast_data):
                    # 두 컬럼으로 나누기
                    left_col, right_col = st.columns([1, 1])  # 두 컬럼으로 나눔
                    with left_col: # 현재 시간을 기준으로 시간, 온도, 날씨 출력(left_col)
                        st.write(f"🕓시간: {forecast['time']}")
                        st.write(f"🌡️온도: {forecast['temp']}°C")
                        st.write(f"☁️날씨: {forecast['description']}")
                    with right_col: # 요일과 그 날 최저, 최고 기온 출력(right_col)
                        weekday_display = (datetime.now() + timedelta(days=i)).strftime("%A")
                        st.write(f"📅요일: {weekday_display}")
                        date_key = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
                        if date_key in daily_min_max:
                            st.write(f"🌡️최저 기온: {daily_min_max[date_key]['temp_min']}°C")
                            st.write(f"🌡️최고 기온: {daily_min_max[date_key]['temp_max']}°C")
                    st.write("------")
            else:
                st.error("날씨 정보를 가져올 수 없습니다.")

    # 추천 일정 출력 (col2)
    with col2:
        st.subheader("📅 추천 일정")
        st.write("chatBot으로 일정 출력하기")

# 메인 실행
if __name__ == "__main__":
    main()
