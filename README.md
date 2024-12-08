# 🧳 춘천 여행 가이드 챗봇

여행 가이드 챗봇은 사용자에게 여행 관련 정보를 제공하는 스마트 도우미입니다.  
여행 계획, 추천 명소 등을 간단한 입력으로 빠르게 확인할 수 있습니다.

### 🤝 팀원 소개 5조
이 프로젝트는 오픈소스SW의 이해 **5조** 팀원들이 협력하여 개발했습니다.

<table>
  <tbody>
    <tr>
      <td align="center"><a href="https://github.com/GithubOfHermes">
        <img src="https://github.com/GithubOfHermes.png?size=100" width="100px;" alt=""/><br /><sub><b>김성열</b></sub></a><br />
      </td>
      <td align="center"><a href="https://github.com/HongRae-Kim">
        <img src="https://github.com/HongRae-Kim.png?size=100" width="100px;" alt=""/><br /><sub><b>김홍래</b></sub></a><br />
      </td>
      <td align="center"><a href="https://github.com/namhegg">
        <img src="https://github.com/namhegg.png?size=100" width="100px;" alt=""/><br /><sub><b>남형석</b></sub></a><br />
      </td>
      <td align="center"><a href="https://github.com/DriedSlime">
        <img src="https://github.com/DriedSlime.png?size=100" width="100px;" alt=""/><br /><sub><b>심건우</b></sub></a><br />
      </td>
      <td align="center"><a href="https://github.com/20227122">
        <img src="https://github.com/20227122.png?size=100" width="100px;" alt=""/><br /><sub><b>윤태근</b></sub></a><br />
      </td>
    </tr>
  </tbody>
</table>


## ✨ 주요 기능
- **🌍 추천 여행지**: 사용자의 관심사에 맞춘 춘천 내 추천 명소를 제공합니다.
  - 자연 경관을 좋아하는 사용자에게는 소양강 스카이워크나 남이섬을 추천할 수 있습니다.

- **🏨 숙소 및 식당 탐색**: 원하는 지역의 인기 숙소와 맛집을 손쉽게 검색할 수 있습니다.
  - 사용자 리뷰, 평점, 위치 정보를 기반으로 최적의 선택지를 제안합니다.
- **☀️ 날씨 예보**: 춘천의 시간별 날씨 예보를 실시간으로 제공합니다. 
  - 날씨 변화를 고려한 여행 계획을 세울 수 있도록 지원합니다.
- **🔍 빠른 검색 버튼**: 주요 카테고리별로 빠르게 접근할 수 있는 버튼을 제공하여 원하는 정보를 신속하게 찾을 수 있습니다.
- **🗺️ 지도 통합**: KaKao 지도 API를 사용하여 검색한 장소의 지도를 실시간으로 표시합니다.

## 🚀 사용 방법
1. **검색어 입력**: 챗봇 창에 검색어를 입력하세요. (예: `"춘천 식당"`, `"춘천 숙소"`, `"춘천 관광지"`)
2. **좌측 탐색 버튼 선택**: 화면 좌측에 위치한 탐색 버튼을 통해 카테고리를 선택하세요.
3. **지도와 추천 일정 활용**: 제공되는 지도와 맞춤형 일정을 참고하여 여행을 완벽히 준비하세요.

## 설치 방법
이 프로젝트는 **Streamlit**을 기반으로 하며, **다양한 API**와 **Ollama 모델**을 통합하여 데이터를 제공합니다.<br>
아래의 단계를 따라 설치 및 실행할 수 있습니다.

### 1. 필수 라이브러리 설치 
먼저 필요한 파이썬 라이브러리를 설치합니다.
```bash
pip install streamlit requests ollama streamlit_option_menu
```

### 2. API 키 설정 
여러 외부 API를 사용하므로 각 서비스의 API 키가 필요합니다.

- **공공데이터포털 API**
  1. [공공데이터포털](https://www.data.go.kr/)에 가입 후 로그인합니다. 
  2. API 서비스 신청을 통해 필요한 데이터셋(맛집, 숙박업소, 관광지 정보 등)을 신청합니다.
  3. 승인 후 발급받은 **서비스 키**를 입력합니다.

- **KaKao 지도 API**
  1. [KaKao Developers](https://developers.kakao.com/)에 가입 후 로그인합니다.
  2. 애플리케이션을 생성하고 지도 API를 활성화합니다.
  3. 발급받은 JavaScript 키를 입력합니다.

- **OpenWeather API**
  1. [OpenWeather](https://openweathermap.org/)에 가입 후 로그인합니다.
  2. API keys 섹션에서 API 키를 생성합니다.
  3. 발급받은 API 키를 입력합니다.

### 3. Ollama 모델 설치 
Ollama 모델은 챗봇의 자연어 처리 기능을 담당하며, 로컬 서버에서 실행되어야 합니다.
  1. **Ollama 설치**: 

## 🔍 추가 참고 사항 
- 이 챗봇은 **춘천 지역**에 대한 정보만 지원합니다.
- **빠른 검색 버튼을** 통해 간편하게 카테고리를 선택하고, 원하는 정보에 바로 접근할 수 있습니다.
- 여행을 준비할 때 추천되는 **일정**과 **장소**를 통해 더 편리하고 즐거운 여행이 가능해집니다.****
