from nonebot import get_driver
from nonebot.log import logger
from pydantic import BaseModel, Extra
from pathlib import Path
from typing import Union, Dict, List
import httpx
try:
    import ujson as json
except ModuleNotFoundError:
    import json

class PluginConfig(BaseModel, extra=Extra.ignore):
    crazy_path: Path = Path(__file__).parent

driver = get_driver()
crazy_config: PluginConfig = PluginConfig.parse_obj(driver.config.dict())

class DownloadError(Exception):
    pass

class ResourceError(Exception):
    pass

async def download_url(url: str) -> Union[httpx.Response, None]:
    async with httpx.AsyncClient() as client:
        for i in range(3):
            try:
                response = await client.get(url)
                if response.status_code != 200:
                    continue
                return response
            except Exception as e:
                logger.warning(f"Error occured when downloading {url}, {i+1}/3: {e}")
    
    logger.warning(f"Abort downloading")
    return None
