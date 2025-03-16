from flask import Flask, jsonify, request, render_template
import requests
import os
from datetime import datetime
from cwa_crawler import get_weather_data, extract_weather_info, main

app = Flask(__name__)
from google_example import get_coordinates
from auto_time import get_nearest_time

def generate_suggestion(weather):
    """ 根據天氣條件決定是否適合拍照，回傳 list """
    suggestions = []
    
    if "雨" in weather or "雷" in weather:
        suggestions.append("🌧️ 天氣不好，今天可能不適合拍照 📷")
    if "晴" in weather or "多雲" in weather:
        suggestions.append("☀️ 天氣不錯！是個適合拍照的好日子 📸")
    if not suggestions:
        suggestions.append("🤔 天氣不明，請根據現場情況決定！")
    
    return suggestions  # ✅ 回傳 list

@app.route('/weather', methods=['GET'])
def get_weather():
    location = request.args.get('location')

    cwa_api_key = os.getenv("CWA_API_KEY")
    query_time = get_nearest_time()
    if cwa_api_key:
        weather_data = get_weather_data(cwa_api_key, location)
        if weather_data:
            weather_info = extract_weather_info(weather_data, location, query_time)
            
            if isinstance(weather_info, list):
                weather_info = weather_info[0]  # 取出第一筆資料

            if "weather" in weather_info:
                suggestions = generate_suggestion(weather_info["weather"])  # ✅ 取得建議 (list)
                return render_template("weather.html", weather_info=weather_info, suggestions=suggestions)
            else:
                return render_template("weather.html", error="天氣資訊格式錯誤，缺少 'weather' 欄位")
        else:
            return render_template("weather.html", error="未找到該區域的天氣資料")
    else:
        return render_template("weather.html", error="請提供有效的 API Key")

    


if __name__ == '__main__':
    app.run(debug=True)

    