import requests
from bs4 import BeautifulSoup
import pandas as pd

# 設定爬取的目標網址
url = "https://goodinfo.tw/tw/StockDividendScheduleList.asp?MARKET_CAT=%E5%85%A8%E9%83%A8&INDUSTRY_CAT=%E5%85%A8%E9%83%A8&YEAR=2024"

# 設定 Headers 模擬瀏覽器訪問
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# 發送 HTTP GET 請求
response = requests.get(url, headers=headers)

# 檢查請求是否成功
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到表格
    table = soup.find('table', {'class': 'solid_1_padding_4_0_tbl'})

    # 解析表格內容
    headers = []
    for th in table.find_all('th'):
        headers.append(th.text.strip())

    rows = []
    for tr in table.find_all('tr')[1:]:  # 跳過表頭行
        cells = tr.find_all('td')
        if len(cells) > 1:  # 確保不是空行
            row = [cell.text.strip() for cell in cells]
            rows.append(row)

    # 將資料轉換為 DataFrame
    df = pd.DataFrame(rows, columns=headers)

    # 將 DataFrame 存為 Excel 檔案
    df.to_excel('StockDividendSchedule.xlsx', index=False)

    print("資料已成功爬取並存為 Excel 檔案！")
else:
    print("無法訪問該網頁。")
