import random
import time
from datetime import datetime
import pandas as pd

from loguru import logger

from app.config import HEADERS_LINEA_URL, USER_AGENTS, WALLETS_INFO, settings
from app.service import get_pages, get_transactions_info

import requests
from bs4 import BeautifulSoup

def main():
    """Main function to run the app and save the data to a xlsx file."""
    time_start = time.time()
    # excel_data = pd.read_excel("data/2024-06-03_17-11-12/output.xlsx")
    
    # for index, row in excel_data.iterrows():
    #     token_address = row['Token Address']
    #     info = {
    #         'sold': row['Sold'],
    #         'bought': row['Bought'],
    #         'day': {
    #             'bought': row['Day Bought'],
    #             'sold': row['Day Sold']
    #         },
    #         'week': {
    #             'bought': row['Week Bought'],
    #             'sold': row['Week Sold']
    #         },
    #         'month': {
    #             'bought': row['Month Bought'],
    #             'sold': row['Month Sold']
    #         },
    #         'url': row['URL'],
    #         'balance_address': row['Balance Adresss USD'],
    #         'balance_token': row['Balance Token USD'],
    #         'liquidity_pool': row['Liquidity Pool USD'],
    #         'followers_balance': row['Followers Balance USD'],
    #         'contract': True
    #     }

    #     # Запись информации в словарь WALLETS_INFO
    #     WALLETS_INFO[token_address] = info

    token_params = {
        'tkn': settings.TOKEN,
        'mtd': settings.METHOD,
        'ps': 100
    }
    
    date_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    data_dir = settings.DATA_DIR / date_str
    data_dir.mkdir(parents=True, exist_ok=True) 

    file_path = data_dir / "output.xlsx"
    
    HEADERS_LINEA_URL['User-Agent'] = random.choice(USER_AGENTS)
    pages = get_pages(requests.get(settings.FILTER_URL, headers=HEADERS_LINEA_URL, params=token_params))
    logger.info(f"pages: {pages} need to be processed")
    
    for page in range(1, pages + 1):
        token_params['p'] = page
        HEADERS_LINEA_URL['User-Agent'] = random.choice(USER_AGENTS)
        time.sleep(1)
        response = requests.get(settings.FILTER_URL, headers=HEADERS_LINEA_URL, params=token_params)
        soup = BeautifulSoup(response.text, 'html.parser')
        get_transactions_info(soup)
        logger.info(f"page {page} processed")
        if page %10 == 0:
            data = []
            for token_address, info in WALLETS_INFO.items():
                if info['balance_token'] < settings.MIN_TOKEN_BALANCE:
                    logger.info(f"Token {token_address} has balance less than {settings.MIN_TOKEN_BALANCE}")
                    continue
                
                if info['balance_address'] < settings.MIN_WALLER_BALANCE:
                    logger.info(f"Token {token_address} has balance less than {settings.MIN_WALLER_BALANCE}")
                    continue
                
                if info['liquidity_pool'] < settings.MIN_LIQUIDITY_POOL:
                    logger.info(f"Token {token_address} has liquidity pool less than {settings.MIN_LIQUIDITY_POOL}")
                    continue
                
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
                    'Contract': 'Yes' if info['contract'] else 'No'
                }
                data.append(row)

            df = pd.DataFrame(data)
            df.to_excel(file_path, index=False)
                
    data = []
    for token_address, info in WALLETS_INFO.items():
        if info['balance_token'] < settings.MIN_TOKEN_BALANCE:
            logger.info(f"Token {token_address} has balance less than {settings.MIN_TOKEN_BALANCE}")
            continue
        
        if info['balance_address'] < settings.MIN_WALLER_BALANCE:
            logger.info(f"Token {token_address} has balance less than {settings.MIN_WALLER_BALANCE}")
            continue
        
        if info['liquidity_pool'] < settings.MIN_LIQUIDITY_POOL:
            logger.info(f"Token {token_address} has liquidity pool less than {settings.MIN_LIQUIDITY_POOL}")
            continue
        
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
            'Contract': 'Yes' if info['contract'] else 'No'
        }
        data.append(row)

    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False)
    
    logger.info(f"Data saved to output.xlsx")
    logger.info(f"Time elapsed: {time.time() - time_start}")

if __name__ == "__main__":
    main()
