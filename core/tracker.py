import uuid
import time
from datetime import datetime
from typing import Dict, Any, List, Optional

class Tracker:
    def __init__(self):
        # In-memory storage for tracking data
        # { 'link_id': { 'target_url': '...', 'clicks': [ {...}, ... ] } }
        self.links: Dict[str, Dict[str, Any]] = {}

    def generate_link(self, target_url: str) -> str:
        link_id = str(uuid.uuid4())[:8]
        self.links[link_id] = {
            'target_url': target_url,
            'created_at': datetime.now().isoformat(),
            'clicks': []
        }
        return link_id

    def log_click(self, link_id: str, client_data: Dict[str, Any]):
        if link_id in self.links:
            # Timestamp formatted as HH:MM:SS for the requested table
            now = datetime.now()
            timestamp = now.strftime("%H:%M:%S")
            
            # Extract IP string (could be multiple from X-Forwarded-For)
            ip_raw = client_data.get('ip', 'Unknown')
            
            # Build Location string
            geo = client_data.get('geo', {})
            location = f"{geo.get('city', '')}, {geo.get('country', '')}".strip(', ')
            if not location: location = "Capturing..."
            
            # Build ISP/UserAgent string
            isp = geo.get('isp', '')
            ua = client_data.get('user_agent', '')
            isp_ua = f"{isp} | {ua}" if isp else ua

            click_entry = {
                'timestamp': timestamp,
                'ip': ip_raw,
                'location': location,
                'isp_ua': isp_ua,
                'full_headers': client_data.get('headers', {}),
                'full_geo': geo
            }
            self.links[link_id]['clicks'].insert(0, click_entry) # Most recent first
            return self.links[link_id]['target_url']
        return None

    def get_link_data(self, link_id: str) -> Optional[Dict[str, Any]]:
        return self.links.get(link_id)

    def get_all_links(self) -> List[Dict[str, Any]]:
        return [{'id': k, **v} for k, v in self.links.items()]
