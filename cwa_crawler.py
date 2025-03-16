import requests
import os
from datetime import datetime
import pytz
def get_weather_data(cwa_api_key: str, location_name: str):
    """
    根據提供的 API key 和位置名稱，從中央氣象局 API 獲取天氣資料。
    這個函數會回傳一個字典，包含該區域的天氣資料。
    """
    header = {'Accept': 'application/json',}
    
    parameters = {
        'Authorization': cwa_api_key,
        'locationName': [location_name]
    }

    url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-073'
    response = requests.get(url, headers=header, params=parameters)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Requests Failed with status code:", response.status_code)
        return None


              
def extract_weather_info(weather_data, location_name, query_time):
    """
    從獲取的天氣資料中提取城市名稱、區域名稱、溫度、天氣現象及降雨機率。
    返回一個字典，包含指定區域的天氣資料。
    """
    weather_info = []

    if weather_data:
        # 迭代所有區域資料
        for location in weather_data['records']['Locations'][0]['Location']:
            city_name = weather_data['records']['Locations'][0]['LocationsName']  # 城市名稱
            district_name = location['LocationName']  # 區域名稱

            # 如果區域名稱與用戶輸入的名稱匹配，則提取資料
            if district_name == location_name:
                temperature = None
                weather = None
                weather_description  = None
                precipitation = None
                
                # 提取溫度與天氣現象資料
                for weather_element in location['WeatherElement']:
                    # 提取溫度
                    if weather_element['ElementName'] == "溫度":
                        for time in weather_element['Time']:
                            temperature = time['ElementValue'][0]['Temperature']

                    # 提取天氣現象
                    if weather_element['ElementName'] == "天氣現象":
                        for time in weather_element['Time']:
                            weather = time['ElementValue'][0]['Weather']
                
                # 提取降雨機率資料
                for weather_element in location['WeatherElement']:
                    if weather_element['ElementName'] == "3小時降雨機率":
                        for time in weather_element['Time']:
                            precipitation = time['ElementValue'][0]['ProbabilityOfPrecipitation']
                            start_time = time['StartTime']
                            # end_time = time['EndTime']

                for weather_element in location["WeatherElement"]:
                    if weather_element["ElementName"] == "天氣預報綜合描述":
                        for time in weather_element["Time"]:  # 這裡才有 "Time"
                            weather_description = time["ElementValue"][0]['WeatherDescription']# 取出天氣描述

                            
                            # 格式化時間
                            start_time_obj = datetime.fromisoformat(start_time[:-6])  # 去掉時區部分
                            # end_time_obj = datetime.fromisoformat(end_time[:-6])  # 去掉時區部分
                            # query_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                            query_time = start_time_obj.strftime("%Y-%m-%d %H:%M")
                            # formatted_end_time = end_time_obj.strftime("%Y-%m-%d %H:%M")

                            weather_info.append({
                                'city_name': city_name,
                                'district_name': district_name,
                                'temperature': temperature,
                                'weather': weather,
                                'precipitation': f"{precipitation}%",
                                'rain_time': query_time,
                                'weather_description': weather_description
                            })
    
    return weather_info


def print_weather_info(weather_info):
    """
    打印整理好的天氣資料。
    """
    if weather_info:
        for info in weather_info:
            print(f"城市: {info['city_name']}, 區域: {info['district_name']}, "
                  f"溫度: {info['temperature']}°C, 天氣現象: {info['weather']}, "
                  f"降雨機率: {info['precipitation']} ({info['rain_time']},"
                  f"天氣描述: {info['weather_description']}"
                  )
    else:
        print("沒有天氣資料可顯示。")


def main():
    """
    主程式，會呼叫上述的函數來獲取並顯示天氣資料。
    """
    cwa_api_key = os.getenv("CWA_API_KEY")  # 你可以將這個值設定為你的 API key
    
    # 讓用戶輸入想查詢的單一區域名稱
    location = input("請輸入想查詢的區域名稱（例如：中區）：").strip()
    

    # 設定台灣時區
    tz = pytz.timezone('Asia/Taipei')
    query_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M")
    if cwa_api_key:
        weather_data = get_weather_data(cwa_api_key, location)
        weather_info = extract_weather_info(weather_data, location, query_time)
        print_weather_info(weather_info)
    else:
        print("請提供有效的 API Key。")


if __name__ == '__main__':
    main()
