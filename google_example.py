

import requests
import os
from cwa_crawler import main
GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")


def get_coordinates(city_name):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={city_name}&key={GOOGLE_MAPS_API_KEY}"
    
    response = requests.get(url)
    data = response.json()
    
    if data["status"] == "OK":
        location = data["results"][0]["geometry"]["location"]
        lat, lng = location["lat"], location["lng"]
        return lat, lng
    else:
        return None, None

# 測試用

city = '台中北區'
lat, lng = get_coordinates(city)
if lat and lng:
    print(f"{city} 的經緯度是：({lat}, {lng})")
else:
    print("找不到該地點")