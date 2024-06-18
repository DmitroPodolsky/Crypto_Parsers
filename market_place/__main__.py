import random
import time
from datetime import datetime
import pandas as pd

from loguru import logger

from market_place.config import HEADERS_LINEA_URL, USER_AGENTS, WALLETS_INFO, settings, TOKEN_ADDRESSES
from market_place.service import get_pages, get_transactions_info


import requests
from bs4 import BeautifulSoup

def main():
    global TOKEN_ADDRESSES
    """Main function to run the app and save the data to a xlsx file."""
    time_start = time.time()
    token_market_place  =  TOKEN_ADDRESSES #['0x6131b5fae19ea4f9d964eac0408e4408b66337b5','0xf081470f5c6fbccf48cc4e5b82dd926409dcdd67','0x9971dba6e18536b0415a6fbbf49d81ab12068ab7','0xfc6a4cd4007c3d24d37114d81a801a56f9536625']
    
    date_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    data_dir = settings.DATA_DIR / date_str
    data_dir.mkdir(parents=True, exist_ok=True) 

    file_path = data_dir / "output.xlsx"
    
    for market_token in token_market_place:
        logger.info(f"Processing market token: {market_token}")
        token_params = {
            'ps': 100,
            'tadd': market_token,
            'fadd': market_token,
            'mtd': '0xa9059cbb~Transfer',
        }

        HEADERS_LINEA_URL['User-Agent'] = random.choice(USER_AGENTS)
        pages = get_pages(requests.get(settings.FILTER_URL, headers=HEADERS_LINEA_URL, params=token_params))
        logger.info(f"pages: {pages} need to be processed")
        if pages == 0:
            pages = 1

        for page in range(1, pages + 1):
            if page == 500:
                break
            token_params['p'] = page
            HEADERS_LINEA_URL['User-Agent'] = random.choice(USER_AGENTS)
            time.sleep(1)
            response = requests.get(settings.FILTER_URL, headers=HEADERS_LINEA_URL, params=token_params)
            try:
                soup = BeautifulSoup(response.text, 'html.parser')
                get_transactions_info(soup, market_token)
            except Exception as e:
                logger.error(f"Error: {e}")
                logger.error(f"Error on page: {page}")
                logger.error(f"Error on market token: {market_token}")
                logger.error(f"Error on response: {response.text}")
                break
            logger.info(f"page {page} processed")
            if page %10 == 0:
                data = []
                for token_address, info in WALLETS_INFO.items():
                    
                    row = {
                        'Token Address': info['address_token'],
                        'Tranzaction links': ', '.join(info['tranzaction_links']),
                        'Market Token': info['market_token'],
                        'Contract': 'Yes' if info['contract'] else 'No',
                        'Count Tranzactions': len(info['tranzaction_links'])
                        }
                    data.append(row)

                df = pd.DataFrame(data)
                df.to_excel(file_path, index=False)

        data = []
        for token_address, info in WALLETS_INFO.items():
            row = {
                'Token Address': info['address_token'],
                'Tranzaction links': ', '.join(info['tranzaction_links']),
                'Market Token': info['market_token'],
                'Contract': 'Yes' if info['contract'] else 'No',
                'Count Tranzactions': len(info['tranzaction_links'])
                }
            data.append(row)
            
        df = pd.DataFrame(data)
        df.to_excel(file_path, index=False)
        logger.info(f"Data saved to output.xlsx, end of processing for market token: {market_token}, Time elapsed: {time.time() - time_start}")
        
    logger.info(f"Data saved to output.xlsx")
    logger.info(f"Time elapsed: {time.time() - time_start}")

if __name__ == "__main__":
    main()