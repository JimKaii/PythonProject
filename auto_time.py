from datetime import datetime, timedelta

current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print("現在時間：", current_time)



def get_nearest_time():
    """ 找到最近的天氣查詢時間 (小時為單位) """
    now = datetime.now()
    current_hour = now.hour

    # 天氣 API 可能是每 3 小時一筆資料，找出最近的時段
    available_hours = [0, 3, 6, 9, 12, 15, 18, 21]
    nearest_hour = min(available_hours, key=lambda x: abs(x - current_hour))

    nearest_time = now.replace(hour=nearest_hour, minute=0, second=0, microsecond=0)
    return nearest_time.strftime("%Y-%m-%d %H:%M:%S")

# 測試看看
print("最近的時段是：", get_nearest_time())
