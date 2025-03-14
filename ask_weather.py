from flask import Flask, jsonify, request, render_template
import requests
import os
from datetime import datetime
from cwa_crawler import get_weather_data, extract_weather_info, print_weather_info

app = Flask(__name__)

@app.route('/weather', methods=['GET'])
def get_weather():
    # 從 GET 請求的參數中獲取區域名稱和查詢時間
    location = request.args.get('location')  # 取得用戶輸入的區域名稱
    query_time = request.args.get('time')    # 取得用戶輸入的查詢時間
    
    if not location or not query_time:
        return render_template("weather.html", error="請提供區域名稱和查詢時間參數")

    cwa_api_key = os.getenv("CWA_API_KEY")  # 取得 API Key

    if cwa_api_key:
        weather_data = get_weather_data(cwa_api_key, location)
        if weather_data:
            weather_info = extract_weather_info(weather_data, location, query_time)  # 傳入查詢時間
            if weather_info:
                return render_template("weather.html", weather_info=weather_info)
            else:
                return render_template("weather.html", error="未找到該區域的天氣資料")
        else:
            return render_template("weather.html", error="天氣資料獲取失敗")
    else:
        return render_template("weather.html", error="請提供有效的 API Key")


if __name__ == '__main__':
    app.run(debug=True)
