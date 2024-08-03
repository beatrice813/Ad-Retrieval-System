pip install requests

import requests
from bs4 import BeautifulSoup
import csv

# 設定目標網站
url = 'https://pmds.fda.gov.tw/illegalad/'

# 發送HTTP請求
response = requests.get(url)

# 檢查請求是否成功
if response.status_code == 200:
    # 解析HTML內容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到廣告案例元素
    cases = soup.find_all('div', class_='case')  # 假設案例信息在<div class='case'>內

    # 打開CSV文件準備寫入
    with open('illegal_ads.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['category', 'title', 'content']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # 提取案例信息並寫入CSV文件
        for case in cases:
            category = case.find('span', class_='category').text.strip()  # 假設類別在<span class='category'>內
            title = case.find('h3').text.strip()  # 假設標題在<h3>內
            content = case.find('p', class_='content').text.strip()  # 假設內容在<p class='content'>內
            writer.writerow({'category': category, 'title': title, 'content': content})

    print("違法廣告數據已成功爬取並保存到illegal_ads.csv文件中")
else:
    print("無法訪問目標網站")

    


