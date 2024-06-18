from datetime import datetime
import re
from bs4 import BeautifulSoup
from requests import Response

from check_liquidities.config import WALLETS_INFO
from check_liquidities.utils import get_addresses


def get_pages(response: Response) -> int:
    """Get the number of pages from the response object."""
    soup = BeautifulSoup(response.text, 'html.parser')

    div_content = soup.find('div', class_='d-flex flex-wrap align-items-center justify-content-between gap-3')

    paragraph_text = div_content.find('p').text.strip()
    match = re.search(r'\d{1,3}(?:,\d{3})*', paragraph_text)
    number_str = match.group().replace(',', '')
    
    return round(int(number_str) / 100)
    
def get_transactions_info(soup: BeautifulSoup, token_address: str) -> None:
    """Get transactions info from the soup object."""
    wallets = soup.find('tbody', class_="align-middle text-nowrap").find_all('tr')
    
    if token_address not in WALLETS_INFO:
        WALLETS_INFO[token_address] = {"claimed": 0, "sold": 0, "date_first_claimed": None, "contract": None}
        
    for wallet_info in wallets:
        # block_number = soup.find('td', class_='advFilterBlockNumber').text
        # if block_number not in BLOCKS_INFO:
        #     BLOCKS_INFO[block_number] = {"sold_adresses": [], "bought_adresses": []}
        span = wallet_info.find('td', class_="advFilterAmount").find('span', {'data-bs-toggle': True})
        balance_str = span['data-bs-title']
        balance_str = balance_str.replace(',', '')
        date = soup.find('td', class_='showDate advFilterAge').find('span').text
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        method = wallet_info.find('td', class_="advFilterMethod").find('span').text
        
        if method == 'Claim Rewards':
            WALLETS_INFO[token_address]['claimed'] += float(balance_str)
            if WALLETS_INFO[token_address]['date_first_claimed'] is None:
                WALLETS_INFO[token_address]['date_first_claimed'] = date
            if WALLETS_INFO[token_address]['contract'] is None:
                WALLETS_INFO[token_address]['contract'] = True if wallet_info.find('td', class_="advFilterFromAddress").find('i', class_="far fa-file-alt text-secondary") else False
            continue
        
        from_token_address, to_token_address = get_addresses(wallet_info)
        
        if from_token_address == token_address and method == 'Swap':
            WALLETS_INFO[token_address]['sold'] += float(balance_str)
            if WALLETS_INFO[token_address]['contract'] is None:
                WALLETS_INFO[token_address]['contract'] = True if wallet_info.find('td', class_="advFilterFromAddress").find('i', class_="far fa-file-alt text-secondary") else False
            
        
        