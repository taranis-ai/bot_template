from typing import Literal
from taranis_base_bot.config import CommonSettings


class Settings(CommonSettings):
    MODEL: Literal[""]
    PACKAGE_NAME: str = "{{package_name}}"
    HF_MODEL_INFO: bool = True
    PAYLOAD_KEY: str = "key"


Config = Settings()
