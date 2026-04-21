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
            click_entry = {
                'timestamp': datetime.now().isoformat(),
                'ip': client_data.get('ip'),
                'user_agent': client_data.get('user_agent'),
                'referer': client_data.get('referer'),
                'headers': client_data.get('headers', {}),
                'geo': client_data.get('geo', {})
            }
            self.links[link_id]['clicks'].append(click_entry)
            return self.links[link_id]['target_url']
        return None

    def get_link_data(self, link_id: str) -> Optional[Dict[str, Any]]:
        return self.links.get(link_id)

    def get_all_links(self) -> List[Dict[str, Any]]:
        return [{'id': k, **v} for k, v in self.links.items()]
