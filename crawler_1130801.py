import requests
from bs4 import BeautifulSoup
import csv

# 設定目標網站
url = 'https://www.fda.gov.tw/TC/news.aspx?cid=5085'

# 發送HTTP請求
response = requests.get(url)

# 檢查請求是否成功
if response.status_code == 200:
    # 解析HTML內容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到廣告案例元素，這裡需要確認實際的HTML結構
    cases = soup.find_all('tr')  # 假設案例信息在<table>的<tr>標籤內

    # 打開CSV文件準備寫入
    with open('illegal_ads.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['category', 'title', 'content']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # 提取案例信息並寫入CSV文件
        for case in cases:
            try:
                category = case.find_all('td')[0].text.strip()  # 假設類別在<td>標籤內
                title = case.find_all('td')[1].text.strip()  # 假設標題在<td>標籤內
                content = case.find_all('td')[2].text.strip()  # 假設內容在<td>標籤內
                writer.writerow({'category': category, 'title': title, 'content': content})
            except (IndexError, AttributeError):
                # 當找不到元素時，跳過該案例
                continue

    print("違法廣告數據已成功爬取並保存到illegal_ads.csv文件中")
else:
    print("無法訪問目標網站")
