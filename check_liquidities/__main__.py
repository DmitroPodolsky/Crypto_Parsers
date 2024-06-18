import random
import time
from datetime import datetime
import pandas as pd

from loguru import logger

from check_liquidities.config import HEADERS_LINEA_URL, USER_AGENTS, WALLETS_INFO, settings, TOKEN_ADDRESSES
from check_liquidities.service import get_pages, get_transactions_info

import requests
from bs4 import BeautifulSoup

def main():
    global TOKEN_ADDRESSES
    """Main function to run the app and save the data to a xlsx file."""
    time_start = time.time()
    
    date_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    data_dir = settings.DATA_DIR / date_str
    data_dir.mkdir(parents=True, exist_ok=True) 

    file_path = data_dir / "output.xlsx"
    
    for token_address in TOKEN_ADDRESSES:
        
        logger.info(f"Processing token: {token_address}")
        token_params = {
            'tkn': settings.TOKEN,
            'ps': 100,
            'tadd': token_address,
            'fadd': token_address,
            'mtd': '0xe21fd0e9~Swap,0x20b1cb6f~Claim+Rewards'
        }

        HEADERS_LINEA_URL['User-Agent'] = random.choice(USER_AGENTS)
        pages = get_pages(requests.get(settings.FILTER_URL, headers=HEADERS_LINEA_URL, params=token_params))
        logger.info(f"pages: {pages} need to be processed")
        if pages == 0:
            pages = 1

        for page in range(1, pages + 1):
            token_params['p'] = page
            HEADERS_LINEA_URL['User-Agent'] = random.choice(USER_AGENTS)
            time.sleep(1)
            response = requests.get(settings.FILTER_URL, headers=HEADERS_LINEA_URL, params=token_params)
            try:
                soup = BeautifulSoup(response.text, 'html.parser')
                get_transactions_info(soup, token_address)
            except Exception:
                WALLETS_INFO[token_address] = {"claimed": 0, "sold": 0, "date_first_claimed": None, "contract": False}
                
            logger.info(f"page {page} processed")
            if page %10 == 0:
                data = []
                for token_address, info in WALLETS_INFO.items():
                    row = {
                        'Token Address': token_address,
                        'Sold': info['sold'],
                        'Claimed': info['claimed'],
                        'Date First Claimed': info['date_first_claimed'],
                        'Contract': 'Yes' if info['contract'] else 'No'
                    }
                    data.append(row)

                df = pd.DataFrame(data)
                df.to_excel(file_path, index=False)

        data = []
        for token_address, info in WALLETS_INFO.items():
            row = {
                'Token Address': token_address,
                'Sold': info['sold'],
                'Claimed': info['claimed'],
                'Date First Claimed': info['date_first_claimed'],
                'Contract': 'Yes' if info['contract'] else 'No'
            }
            data.append(row)
            
        df = pd.DataFrame(data)
        df.to_excel(file_path, index=False)

        logger.info(f"Data saved to output.xlsx, processed token: {token_address}, time elapsed: {time.time() - time_start}")
        logger.info(f"Time elapsed: {time.time() - time_start}")

if __name__ == "__main__":
    main()
