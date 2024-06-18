from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

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