# app.py
from datetime import datetime
from flask import Flask, render_template, request, jsonify
import os
from cwa_crawler import get_weather_data, extract_weather_info, print_weather_info  # 導入 weather.py 中的函數
import requests
from chatgpt_example import chat_with_chatgpt
app = Flask(__name__)

# 環境變數中取得 CWA API key
CWA_API_KEY = os.getenv("CWA_API_KEY")
# Google Geocoding API Key
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")  # 使用你的 Google Maps API 金鑰
render_template
# 模擬的經緯度資料，可以換成實際的資料來源
coordinates = {
    '中區': {'lat': 24.1469, 'lng': 120.6832},
    '東區': {'lat': 24.1460, 'lng': 120.7219},
    '南區': {'lat': 24.1411, 'lng': 120.6744},
    '西區': {'lat': 24.1439, 'lng': 120.6627},
    '北區': {'lat': 24.1644, 'lng': 120.6830},
    '西屯區': {'lat': 24.1686, 'lng': 120.6418},
    '南屯區': {'lat': 24.1429, 'lng': 120.6547},
    '北屯區': {'lat': 24.1790, 'lng': 120.6870},
    '太平區': {'lat': 24.1417, 'lng': 120.7210},
    '大里區': {'lat': 24.2203, 'lng': 120.6822},
    '霧峰區': {'lat': 24.1850, 'lng': 120.7377},
    '烏日區': {'lat': 24.1456, 'lng': 120.5835},
    '豐原區': {'lat': 24.2615, 'lng': 120.7320},
    '后里區': {'lat': 24.3092, 'lng': 120.7064},
    '石岡區': {'lat': 24.2545, 'lng': 120.7463},
    '東勢區': {'lat': 24.2956, 'lng': 120.8577},
    '大甲區': {'lat': 24.3153, 'lng': 120.6161},
    '清水區': {'lat': 24.3180, 'lng': 120.4533},
    '沙鹿區': {'lat': 24.2357, 'lng': 120.5955},
    '梧棲區': {'lat': 24.2355, 'lng': 120.5033},
    '龍井區': {'lat': 24.2074, 'lng': 120.5374},
    '大肚區': {'lat': 24.2117, 'lng': 120.5529},
    '大安區': {'lat': 24.4244, 'lng': 120.4916},
    '健行區': {'lat': 24.1821, 'lng': 120.7607},
    '大雅區': {'lat': 24.2554, 'lng': 120.6157},
    '神岡區': {'lat': 24.2965, 'lng': 120.6847},
    '新社區': {'lat': 24.2701, 'lng': 120.8912}
}


def get_coordinates(city_name):
    """
    根據城市名稱使用 Google Geocoding API 查詢經緯度
    """
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={city_name}&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if data["status"] == "OK":
        location = data["results"][0]["geometry"]["location"]
        lat = location["lat"]
        lng = location["lng"]
        return lat, lng
    else:
        return None, None
    
@app.route('/')
def index():
    return render_template('index.html')  # 這裡你可以設置你的首頁

@app.route('/get_coordinates', methods=['GET'])
def get_coordinates():
    
    city_name = request.args.get('city_name')
    if city_name in coordinates:
        return {
            'latitude': coordinates[city_name]['lat'],
            'longitude': coordinates[city_name]['lng'],
            'city': city_name,
            
        }
    else:
        return {'error': 'City not found'}

@app.route('/weather')
def weather():

    city = request.args.get('city')
    lat = float(request.args.get('lat'))
    lng = float(request.args.get('lng'))

    if not city or not lat or not lng:
        return jsonify({"error": "缺少參數"}), 400
    
    # 這裡你可以根據經緯度獲取天氣資料
    # 假設你已經有 get_weather_data 和 extract_weather_info 函數
    weather_data = get_weather_data(CWA_API_KEY, city)  # 你需要根據城市名稱來查詢天氣資料
    weather_info = extract_weather_info(weather_data, city, None)

    weather_condition = weather_info[0]['weather']
    # reponse = chat_with_chatgpt(
    #     user_message=weather_condition, 
    #     system_prompt='你是一個專業且具有創造力的攝影師，'
    #     '能夠依照'f'{city}的周圍,{weather_condition}''天氣來決定拍攝的模式，並且精簡的列出格式如下'
    #     '先簡單描述一段天氣狀況'
    #     '是否該前往:'
    #     '適合的景點:列出五項' 
    #     '建議的攝影風格:'
    #     '色調及技術:'
    #     '，其餘的不需要顯示')

    if '雨' in weather_condition:
        shooting_advice =  "有可能會下雨，建議拍攝雨景或雲霧景色。"
    elif '晴' in weather_condition:
        shooting_advice =  "今天是晴天，建議拍攝日出或日落，或是戶外風景。"
    elif '多雲' in weather_condition:
        shooting_advice = "天是陰天，適合拍攝柔和光線的風景或室內場景。"
    else:
        shooting_advice = "氣條件不明，您可以嘗試多種拍攝風格。"



    return render_template('weather_info.html', 
        city_name=city,
        weather_info=weather_info,
        lat=lat, lng=lng,
        locations=coordinates.keys(),
        shooting_advice=shooting_advice,
        GOOGLE_MAPS_API_KEY=GOOGLE_MAPS_API_KEY
        # reponse=reponse
        
    )
   


if __name__ == '__main__':
    app.run(debug=True)
