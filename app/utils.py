import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from app.config import WALLETS_INFO, settings

def get_addresses(soup: BeautifulSoup) -> None:
    """Get addresses from the soup object."""
    a_tag = soup.find('td', class_="advFilterFromAddress").find('a', {'data-highlight-target': True})
    from_token_address = a_tag['data-highlight-target']
    a_tag = soup.find('td', class_="advFilterToAddress").find('a', {'data-highlight-target': True})
    to_token_address = a_tag['data-highlight-target']
    
    return from_token_address, to_token_address

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

def create_wallet_info(token_address: str, wallet_info: BeautifulSoup) -> None:
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Режим headless
    chrome_options.add_argument("--disable-gpu")  # Отключение GPU (некоторые версии headless требуют этого)
    chrome_options.add_argument("--no-sandbox")  # Отключение песочницы
    chrome_options.add_argument("--disable-dev-shm-usage")  # Отключение shared memory
    # Инициализация WebDriver с настройками
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url=settings.DEBANK_URL + token_address)
    time.sleep(10)  # Ожидание загрузки страницы
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
    
    contract = True
    if not wallet_info.find('i', class_="far fa-file-alt text-secondary"):
        contract = False
    
        
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
        'contract': contract
    }