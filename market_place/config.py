from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict
import pandas as pd

project_dir = Path(__file__).parent.parent


class Settings(BaseSettings):
    """
    Class for storing app settings.
    """

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)
    DATA_DIR: Path = project_dir / "data"

    FILTER_URL: str = "https://lineascan.build/advanced-filter"
    DEBANK_URL: str = "https://debank.com/profile/"
    MIN_WALLER_BALANCE: float = 0.0
    MIN_TOKEN_BALANCE: float = 0.0
    MIN_LIQUIDITY_POOL: float = 0.0
    METHOD: str
    TOKEN: str


settings = Settings()

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-A505FN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/90.0.818.56",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
]

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

WALLETS_INFO = {}
file_path_1 = 'foldert/filtered_output_balance.xlsx'
df1 = pd.read_excel(file_path_1)
# # Load the second Excel file
# file_path_2 = 'foldert/filtered_liquidity.xlsx'
# df2 = pd.read_excel(file_path_2)
# Extract the 'Token Address' columns
tokens1 = df1['Token Address'].tolist()
# tokens2 = df2['Token Address'].tolist()
# Combine the tokens and remove duplicates
TOKEN_ADDRESSES = tokens1 # list(set(tokens1 + tokens2))