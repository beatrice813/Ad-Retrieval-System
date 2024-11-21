import requests
from bs4 import BeautifulSoup
import csv
import time

# 設定目標網站的基礎 URL
base_url = 'https://www.fda.gov.tw/TC/news.aspx?cid=5085&page={}'

# 設定目標資料量
target_count = 500
max_pages = 50

# 初始化數據列表
all_cases = []

# 從第 1 頁開始抓取，直到第 50 頁或收集到 500 筆資料
for page in range(1, max_pages + 1):
    # 建立每頁的完整URL
    url = base_url.format(page)

    # 發送HTTP請求
    response = requests.get(url)

    # 檢查請求是否成功
    if response.status_code != 200:
        print(f"無法訪問頁面 {page}，狀態碼: {response.status_code}")
        break

    # 解析HTML內容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到廣告案例元素，這裡需要確認實際的HTML結構
    cases = soup.find_all('tr')  # 假設案例信息在<table>的<tr>標籤內

    # 提取每個案例的信息並存入 all_cases
    for case in cases[:10]:  # 每頁最多處理 10 筆數據
        if len(all_cases) >= target_count:
            break

        try:
            category = case.find_all('td')[0].text.strip()  # 假設類別在<td>標籤內
            title = case.find_all('td')[1].text.strip()  # 假設標題在<td>標籤內
            content = case.find_all('td')[2].text.strip()  # 假設內容在<td>標籤內
            all_cases.append({'category': category, 'title': title, 'content': content})
        except (IndexError, AttributeError):
            # 當找不到元素時，跳過該案例
            continue

    print(f"已從第 {page} 頁抓取數據，累計抓取數據量：{len(all_cases)}")

    # 如果已經達到目標數量，提前停止
    if len(all_cases) >= target_count:
        break

    # 延遲請求，以避免對伺服器的壓力過大
    time.sleep(1)

# 寫入CSV文件
with open('illegal_ads.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    fieldnames = ['category', 'title', 'content']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_cases)

print(f"違法廣告數據已成功爬取並保存到illegal_ads.csv文件中，共爬取 {len(all_cases)} 筆數據。")
