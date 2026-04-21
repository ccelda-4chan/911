import aiohttp
from typing import Dict, Any, Optional

class OSINT:
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None

    async def get_session(self) -> aiohttp.ClientSession:
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5))
        return self.session

    async def ip_lookup(self, ip: str) -> Dict[str, Any]:
        """Lookup IP address information using ip-api.com."""
        try:
            session = await self.get_session()
            async with session.get(f"http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query") as resp:
                if resp.status == 200:
                    return await resp.json()
                return {"status": "fail", "message": f"HTTP {resp.status}"}
        except Exception as e:
            return {"status": "fail", "message": str(e)}

    async def phone_carrier_lookup(self, phone: str, prefixes: Dict[str, str]) -> Dict[str, Any]:
        """Identify carrier and network details for Philippine numbers."""
        phone = phone.strip().replace(' ', '').replace('+', '')
        if phone.startswith('63'):
            phone = '0' + phone[2:]
        
        prefix = phone[:4]
        carrier = prefixes.get(prefix, "Unknown / International")
        
        # Simulated Rate Limit effectiveness check
        # High effectiveness if it's a mobile prefix (09XX)
        effectiveness = "HIGH" if prefix.startswith('09') else "MEDIUM"
        
        return {
            "phone": phone,
            "prefix": prefix,
            "carrier": carrier,
            "region": "Philippines (PH)",
            "is_ph": prefix.startswith('09') or prefix.startswith('9'),
            "effectiveness": effectiveness,
            "rate_limit_score": 95 if effectiveness == "HIGH" else 45
        }

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()
