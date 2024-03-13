from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(".env")


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Load plugin credentials from environment
    user_id: str = Field(..., alias="USERALE_USER_ID")
    password: str = Field(..., alias="USERALE_PASSWORD")
    url: str = Field(..., alias="USERALE_ENDPOINT")

    # constants
    timeout_ms: int = Field(5000, alias="TIMEOUT_MS")
    closeout_ms: int = Field(15000, alias="CLOSEOUT_MS")
    path_to_extension: str = Field(..., alias="PATH_TO_EXTENSION")
    user_data_dir: str = Field(..., alias="USER_DATA_DIR")


cfg = Config()
