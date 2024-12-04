import requests
import pandas as pd

# Kakao API endpoint and headers
url = "https://dapi.kakao.com/v2/local/search/address.json"
headers = {
    "Authorization": "KakaoAK 94725ef93944f848cca35aa808d1deee",
    "KA": "python/v1.0 AppName"
}
params = {"query": "춘천시"}

# Send the API request
response = requests.get(url, headers=headers, params=params)

# Handle the response
if response.status_code == 200:
    data = response.json()
    documents = data.get("documents", [])
    df = pd.DataFrame(documents)
    print(df.head())
else:
    print(f"Error: {response.status_code}, {response.json()}")
