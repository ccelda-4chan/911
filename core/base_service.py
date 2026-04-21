import aiohttp
import asyncio
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from utils.logger import logger
from utils.config import config

class BaseService(ABC):
    def __init__(self, name: str):
        self.name = name
        self.logger = logger.getChild(name)

    @abstractmethod
    async def send(self, session: aiohttp.ClientSession, phone: str) -> bool:
        pass

    def normalize_phone(self, phone: str) -> str:
        phone = phone.replace(' ', '')
        if phone.startswith('0'):
            return '+63' + phone[1:]
        elif phone.startswith('63') and not phone.startswith('+63'):
            return '+' + phone
        elif not phone.startswith('+63') and len(phone) == 10:
            return '+63' + phone
        elif not phone.startswith('+'):
            return '+63' + phone
        return phone

    def format_number_no_plus(self, phone: str) -> str:
        return self.normalize_phone(phone).replace('+', '')

    async def _post(self, session: aiohttp.ClientSession, url: str, **kwargs) -> bool:
        try:
            if 'timeout' not in kwargs:
                kwargs['timeout'] = aiohttp.ClientTimeout(total=10)
            
            async with session.post(url, **kwargs) as response:
                status = response.status
                text = await response.text()
                
                if status < 400:
                    self.logger.debug(f"Request to {url} successful: {status}")
                    return True
                else:
                    self.logger.warning(f"Request to {url} failed: {status} - {text[:100]}")
                    return False
        except aiohttp.ClientError as e:
            self.logger.error(f"Network error for {url}: {str(e)}")
        except asyncio.TimeoutError:
            self.logger.error(f"Timeout for {url}")
        except Exception as e:
            self.logger.exception(f"Unexpected error for {url}: {str(e)}")
        return False
