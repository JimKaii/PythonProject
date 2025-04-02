# A Tools for Photography Travel



### 🌤️ Weather Info WEB
🚀 這是一個基於 Flask 的天氣資訊應用，包含爬蟲、後端 API 和前端展示頁面。  
使用者可以透過前端查詢天氣，後端提供 API，並透過爬蟲取得最新的天氣數據。
***


### 下載 API 金鑰
1️⃣ 取得 中央氣象局（CWA）API Key
前往 中央氣象局開放平台 註冊並取得 API Key。

2️⃣ 申請 Google Maps API Key
前往 Google Cloud Console 啟用 Maps API 並取得 API Key。
***

### 安裝與使用

 準備環境
請確保你的系統已安裝 Python 3.x，然後安裝必要的套件：
pip install -r requirements.txt
***

 ### 操作方式
 #### 檢查 API Key
請在對應的程式碼中填入 API Key：

1️⃣ cwa_crawler.py

CWA_API_KEY = "你的中央氣象局 API Key"

2️⃣ flask_ask_weather.py

GOOGLE_MAPS_API_KEY = "你的 Google Maps API Key"

3️⃣templates/text.html

請在 HTML 文件的最後填入 Google API Key
<script src="https://maps.googleapis.com/maps/api/js?key=你的GoogleAPIKey"></script>
***


### 執行專案

1️⃣ 執行爬蟲程式（獲取最新天氣資訊）
python cwa_crawler.py

2️⃣ 啟動 Flask 伺服器
python flask_ask_weather.py

3️⃣ 伺服器啟動後，會顯示類似以下的網址：
http://127.0.0.1:5000
按住 Ctrl + 滑鼠點擊 這個網址，即可打開網頁介面！
***

### 頁面概述

區域類型、區域選擇

<img src="https://drive.google.com/uc?export=view&id=1Po2SJwE11-eyn8nZIRbxKHsDU92YQT42" width="600">


天氣資訊

<img src="https://drive.google.com/uc?export=view&id=1679LVk_3nM9qLUNrhh5Jj85XLkkLi3Hw" width="600">


地圖規劃

<img src="https://drive.google.com/uc?export=view&id=1R1bBpCFOZvJpyzr0ijirDeENe1L1haIL" width="500">


拍攝建議 

<img src="https://drive.google.com/uc?export=view&id=1p7BQFPj8s5hzvRPOCd0x1UTITXY4FBG8" width="500"> 

小助手

<img src="https://drive.google.com/uc?export=view&id=18RtZY-fePMO1PZsPWkMSIO_0cw7s7Upb" width="250">                                                                                        

***            


 ### 技術棧
後端：Flask

爬蟲：Requests

前端：HTML, CSS, JavaScript, Google Maps API



















