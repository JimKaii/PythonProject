# app.py

from flask import Flask, render_template, request, jsonify
import os
from cwa_crawler import get_weather_data, extract_weather_info, print_weather_info  # 導入 weather.py 中的函數
import requests
app = Flask(__name__)

# 環境變數中取得 CWA API key
CWA_API_KEY = os.getenv("CWA_API_KEY")
# Google Geocoding API Key
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")  # 使用你的 Google Maps API 金鑰

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
def get_coordinates_route():
    city_name = request.args.get('city_name')
    
    if not city_name:
        return jsonify({"error": "請提供城市名稱"}), 400

    # 使用 Google Geocoding API 查詢經緯度
    lat, lng = get_coordinates(city_name)
    
    if lat and lng:
        return jsonify({
            "city": city_name,
            "latitude": lat,
            "longitude": lng
        })
    else:
        return jsonify({"error": "找不到該區域"}), 404

@app.route('/weather')
def weather():
    city = request.args.get('city')
    lat = request.args.get('lat')
    lng = request.args.get('lng')

    if not city or not lat or not lng:
        return jsonify({"error": "缺少參數"}), 400

    # 這裡你可以根據經緯度獲取天氣資料
    # 假設你已經有 get_weather_data 和 extract_weather_info 函數
    weather_data = get_weather_data(CWA_API_KEY, city)  # 你需要根據城市名稱來查詢天氣資料
    weather_info = extract_weather_info(weather_data, city, None)

    return render_template('weather_info.html', city_name=city, weather_info=weather_info)

if __name__ == '__main__':
    app.run(debug=True)
