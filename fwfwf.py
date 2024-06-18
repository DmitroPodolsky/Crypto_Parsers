# import pandas as pd

# # Чтение исходного Excel файла
# input_file = 'wallets_info.xlsx'  # замените на путь к вашему файлу
# df = pd.read_excel(input_file)

# # Фильтрация данных по условию liquidity_pool > 50000
# filtered_df = df[df['Balance Token USD'] * 1.75 > 25000]

# # Сохранение отфильтрованных данных в новый Excel файл
# output_file = 'filtered_output.xlsx'  # замените на желаемое имя файла
# filtered_df.to_excel(output_file, index=False)

# print(f"Отфильтрованные данные сохранены в файл {output_file}")

# import pandas as pd

# Чтение данных из исходного Excel файла
# input_file = 'wallets_info.xlsx'  # замените на путь к вашему файлу
# df = pd.read_excel(input_file)

# # Фильтрация данных по условию Liquidity Pool USD > 50000
# filtered_df = df[df['Liquidity Pool USD'] > 50000]

# # Создание новой таблицы с нужными колонками
# result_df = filtered_df[[
#     'Token Address',
#     'URL',
#     'Balance Token USD',
#     'Balance Adresss USD',
#     'Liquidity Pool USD',
#     'Followers Balance USD',
#     'Contract'
# ]]

# # Сохранение отфильтрованных данных в новый Excel файл
# output_file = 'filtered_output.xlsx'  # замените на желаемое имя файла
# result_df.to_excel(output_file, index=False)

# print(f"Фильтрованные данные сохранены в файл {output_file}")

HEADERS_LINEA_URL =  {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Content-Type": "application/json; charset=UTF-8",
        "Cache-Control": "no-cache",
        'Cookie': '_ga=GA1.1.1172355291.1714659807; lineascan_offset_datetime=+3; lineascan_cookieconsent=True; cf_clearance=o9OjFRWoYDK6dBWjxhKhtYmD.W3saUoxAOxtUW7vy7A-1715981895-1.0.1.1-jeu.ErTVQ31tAP3Rut8YPQAlOySR2tMkc0eOveIktEbhxY.R9GBCn7GYuKOWzKtSrAY2SXRupoXrDVzPeNriZA; ASP.NET_SessionId=q2qflt4rkcc5ykxtrw2mwvk4; _ga_7HXXHXN492=GS1.1.1717653095.33.1.1717654536.0.0.0',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        'Priority': 'u=0, i',
        'Sec-Ch-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'Sec-Ch-Ua-Arch': '"x86"',
        'Sec-Ch-Ua-Bitness': '"64"',
        'Sec-Ch-Ua-Full-Version': '"125.0.6422.142"',
        'Sec-Ch-Ua-Full-Version-List': '"Google Chrome";v="125.0.6422.142", "Chromium";v="125.0.6422.142", "Not.A/Brand";v="24.0.0.0"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Model': '""',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Ch-Ua-Platform-Version': '"10.0.0"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
    }

import time
import pandas as pd
import requests
from bs4 import BeautifulSoup

excel_data = pd.read_excel("data/2024-06-17_23-33-50/output.xlsx")

data = []
for index, row in excel_data.iterrows():
    time.sleep(1)
    responce1 = requests.get(f'https://lineascan.build/address/{row["Token Address"]}', headers=HEADERS_LINEA_URL)
    time.sleep(1)
    responce2 = requests.get(f'https://lineascan.build/address/{row["Market Token"]}', headers=HEADERS_LINEA_URL)
    
    soup = BeautifulSoup(responce1.text, 'html.parser')
    answer1 = soup.find("h1", class_="h5 mb-0").text.strip()
    soup = BeautifulSoup(responce2.text, 'html.parser')
    answer2 = soup.find("h1", class_="h5 mb-0").text.strip()
    if answer1 == "Contract" or answer2 == "Contract":
        row['Contract'] = 'Yes'
    else:
        row['Contract'] = 'No'
    data.append(row)
    print(index)
    
df = pd.DataFrame(data)
df.to_excel("wallets_info_with_contract.xlsx", index=False)
print("Data saved to wallets_info_with_contract.xlsx")
    
    
    
