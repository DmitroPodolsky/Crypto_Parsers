from datetime import datetime, timedelta
import re
from bs4 import BeautifulSoup
from requests import Response

from market_place.config import WALLETS_INFO, TOKEN_ADDRESSES
from market_place.utils import get_addresses


def get_pages(response: Response) -> int:
    """Get the number of pages from the response object."""
    soup = BeautifulSoup(response.text, 'html.parser')

    div_content = soup.find('div', class_='d-flex flex-wrap align-items-center justify-content-between gap-3')

    paragraph_text = div_content.find('p').text.strip()
    match = re.search(r'\d{1,3}(?:,\d{3})*', paragraph_text)
    number_str = match.group().replace(',', '')
    
    return round(int(number_str) / 100)
    
def get_transactions_info(soup: BeautifulSoup, market_token: str) -> None:
    """Get transactions info from the soup object."""
    wallets = soup.find('tbody', class_="align-middle text-nowrap").find_all('tr')
    for wallet_info in wallets:
        date = soup.find('td', class_='showDate advFilterAge').find('span').text
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        link_tag = soup.find('a', class_='hash-tag text-truncate myFnExpandBox_searchVal')
        link = 'https://lineascan.build' + link_tag['href']
        
        from_token_address, to_token_address = get_addresses(wallet_info)
        
        if from_token_address in TOKEN_ADDRESSES and from_token_address != market_token:
            contract = wallet_info.find('td', class_="advFilterFromAddress").find('i', class_="far fa-file-alt text-secondary")
            if from_token_address + market_token not in WALLETS_INFO.keys():
                if not contract:
                    WALLETS_INFO[from_token_address + market_token] = {
                    'address_token': from_token_address,
                    'market_token': market_token,
                    'tranzaction_links': [link],
                    'contract': False}
            else:
                WALLETS_INFO[from_token_address + market_token]['tranzaction_links'].append(link)
        
        if to_token_address in TOKEN_ADDRESSES and to_token_address != market_token:
            contract = wallet_info.find('td', class_="advFilterToAddress").find('i', class_="far fa-file-alt text-secondary")
            if to_token_address + market_token not in WALLETS_INFO.keys():
                if not contract:
                    WALLETS_INFO[to_token_address + market_token] = {
                    'address_token': to_token_address,
                    'market_token': market_token,
                    'tranzaction_links': [link],
                    'contract': False}
            else:
                WALLETS_INFO[to_token_address + market_token]['tranzaction_links'].append(link)
            
        
        # if date.date() == datetime.now().date():
        #     WALLETS_INFO[from_token_address]['day']['sold'] += balance
        #     WALLETS_INFO[to_token_address]['day']['bought'] += balance
        
        # if date.date() >= datetime.now().date().replace(day=1):
        #     WALLETS_INFO[from_token_address]['month']['sold'] += balance
        #     WALLETS_INFO[to_token_address]['month']['bought'] += balance
        
        # seven_days_ago = datetime.now() - timedelta(days=7)
        # if date.date() >= seven_days_ago.date():
        #     WALLETS_INFO[from_token_address]['week']['sold'] += balance
        #     WALLETS_INFO[to_token_address]['week']['bought'] += balance
        # # if from_token_address not in BLOCKS_INFO[block_number]['sold_adresses']:
        # #     BLOCKS_INFO[block_number]['sold_adresses'].append(from_token_address)
        # # if to_token_address not in BLOCKS_INFO[block_number]['bought_adresses']:
        # #     BLOCKS_INFO[block_number]['bought_adresses'].append(to_token_address)

        # WALLETS_INFO[from_token_address]['sold'] += balance
        # WALLETS_INFO[to_token_address]['bought'] += balance