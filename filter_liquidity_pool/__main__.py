from loguru import logger
import pandas as pd
import requests
from filter_liquidity_pool.config import settings
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


WALLETS_INFO = {}

excel_data = pd.read_excel("wallets_info.xlsx")
    
for index, row in excel_data.iterrows():
    token_address = row['Token Address']
    info = {
        'sold': row['Sold'],
        'bought': row['Bought'],
        'day': {
            'bought': row['Day Bought'],
            'sold': row['Day Sold']
        },
        'week': {
            'bought': row['Week Bought'],
            'sold': row['Week Sold']
        },
        'month': {
            'bought': row['Month Bought'],
            'sold': row['Month Sold']
        },
        'url': row['URL'],
        'balance_address': row['Balance Adresss USD'],
        'balance_token': row['Balance Token USD'],
        'liquidity_pool': row['Liquidity Pool USD'],
        'followers_balance': row['Followers Balance USD'],
        'contract': True
    }
    # Запись информации в словарь WALLETS_INFO
    WALLETS_INFO[token_address] = info
    
responce = requests.get(f'https://api.w3w.ai/linea/v2/explorer/token/{settings.TOKEN}/top_holders?page=1&size=50000')
data = responce.json()

def get_lequidity_pool(soup: BeautifulSoup) -> int:
    tokens = soup.find_all("div", class_="Project_project__GCrhx")
    for token in tokens:
        if token.find("div", id='linea_thenile'):
            panels = token.find_all("div", class_="Panel_container__Vltd1")
            for panel in panels:
                info = panel.find("div", class_="BookMark_bookmark__UG5a4")
                if info.text == "Liquidity Pool":
                    total_usd_value = 0
                    liquidities = panel.find_all("div", class_="table_contentRow__Mi3k5 flex_flexRow__y0UR2")
                    for liquidity in liquidities:
                        total_usd_value_elem = liquidity.select_one('.table_contentRow__Mi3k5 > div:last-child > span')
                        total_usd_value_str = total_usd_value_elem.text.strip()
                        total_usd_value_str = total_usd_value_str.replace('$', '').replace(',', '')
                        total_usd_value += float(total_usd_value_str)

                    return total_usd_value
            return 0
    return 0

COUNT = 0
for index,adress in enumerate(data['data']):
    if adress['wallet_address'] in WALLETS_INFO:
        continue
    token_address = adress['wallet_address']
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Режим headless
    chrome_options.add_argument("--disable-gpu")  # Отключение GPU (некоторые версии headless требуют этого)
    chrome_options.add_argument("--no-sandbox")  # Отключение песочницы
    chrome_options.add_argument("--disable-dev-shm-usage")  # Отключение shared memory

    # Инициализация WebDriver с настройками
    time.sleep(25)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url=settings.DEBANK_URL + token_address)
    time.sleep(8)  # Ожидание загрузки страницы
    html_document = driver.page_source
    driver.quit()
    url = settings.DEBANK_URL + token_address
    lequidity_pool_value = 0
    followers_balance = 0
    try:
        soup = BeautifulSoup(html_document, "html.parser")
        lequidity_pool_value = get_lequidity_pool(soup)
        followers_balance = soup.find("div", class_="HeaderInfo_value__7Nj3p").text
    except Exception as e:
        print(e)
    
    try:
        balance_address = soup.find("div", class_="projectTitle-number").text
        balance_address = balance_address.replace(',', '').replace('$', '')
        balance_address = float(balance_address)
        balance_tokens = soup.find("div", class_="db-table TokenWallet_table__bmN1O").find_all("div", class_="db-table-wrappedRow")
        target_balance = 0
        for balance_token in balance_tokens:
            token_link = balance_token.find('a', href=True)
            if token_link and settings.TOKEN in token_link['href']:
                balance_cell = balance_token.find_all('div', class_='db-table-cell')[2]
                balance_str = balance_cell.text.strip()
                target_balance = float(balance_str.replace(',', ''))
                break
    except Exception as e:
        balance_address = 0
        target_balance = 0
        url = "empty"

    
        
    WALLETS_INFO[token_address] = {
            'sold': 0,
            'bought': 0,
            'day': {'bought': 0, 'sold': 0},
            'week': {'bought': 0, 'sold': 0},
            'month': {'bought': 0, 'sold': 0},
            'url': url,
            'balance_address': balance_address,
            'balance_token': target_balance,
            'liquidity_pool': lequidity_pool_value,
            'followers_balance': followers_balance,
            'contract': '-'
        }
    logger.info(f"wallet {adress['wallet_address']} processed with index {index}")
    COUNT += 1
    
    if COUNT % 30 == 0:
        data = []
        for token_address, info in WALLETS_INFO.items():
            row = {
                    'Token Address': token_address,
                    'Sold': info['sold'],
                    'Bought': info['bought'],
                    'Day Bought': info['day']['bought'],
                    'Day Sold': info['day']['sold'],
                    'Week Bought': info['week']['bought'],
                    'Week Sold': info['week']['sold'],
                    'Month Bought': info['month']['bought'],
                    'Month Sold': info['month']['sold'],
                    'URL': info['url'],
                    'Balance Token USD': info['balance_token'],
                    'Balance Adresss USD': info['balance_address'],
                    'Liquidity Pool USD': info['liquidity_pool'],
                    'Followers Balance USD': info['followers_balance'],
                    'Contract': info['contract']
                }
            
            data.append(row)
        df = pd.DataFrame(data)
        # Сохранение DataFrame в Excel
        excel_file = 'wallets_info.xlsx'
        df.to_excel(excel_file, index=False)
        print(f"Data saved to {excel_file}")
    
data = []
for token_address, info in WALLETS_INFO.items():
    row = {
            'Token Address': token_address,
            'Sold': info['sold'],
            'Bought': info['bought'],
            'Day Bought': info['day']['bought'],
            'Day Sold': info['day']['sold'],
            'Week Bought': info['week']['bought'],
            'Week Sold': info['week']['sold'],
            'Month Bought': info['month']['bought'],
            'Month Sold': info['month']['sold'],
            'URL': info['url'],
            'Balance Token USD': info['balance_token'],
            'Balance Adresss USD': info['balance_address'],
            'Liquidity Pool USD': info['liquidity_pool'],
            'Followers Balance USD': info['followers_balance'],
            'Contract': info['contract']
        }
    
    data.append(row)
df = pd.DataFrame(data)
# Сохранение DataFrame в Excel
excel_file = 'wallets_info.xlsx'
df.to_excel(excel_file, index=False)
print(f"Data saved to {excel_file}")
    
