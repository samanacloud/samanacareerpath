from datetime import datetime, timedelta
import json
from typing import Any, Dict, Optional

class Storage:
    def __init__(self):
        self._storage: Dict[str, Any] = {}
        
    def get_item(self, key: str) -> Optional[Any]:
        """Get item from storage"""
        return self._storage.get(key, None)
    
    def set_item(self, key: str, value: Any) -> None:
        """Set item in storage"""
        self._storage[key] = value
        
    def remove_item(self, key: str) -> None:
        """Remove item from storage"""
        self._storage.pop(key, None)
        
    def set_with_ttl(self, key: str, value: Any, ttl_seconds: int) -> None:
        """Set item with time-to-live (TTL)"""
        expiry = datetime.now() + timedelta(seconds=ttl_seconds)
        self._storage[key] = {
            'value': value,
            'expiry': expiry.isoformat()
        }
        
    def get_with_ttl(self, key: str) -> Optional[Any]:
        """Get item with TTL, returns None if expired"""
        item = self._storage.get(key, None)
        if item and datetime.now() < datetime.fromisoformat(item['expiry']):
            return item['value']
        self.remove_item(key)
        return None
    
    def to_json(self) -> str:
        """Convert storage contents to JSON string"""
        return json.dumps(self._storage, indent=2, default=str)

# Create instances for local and session storage
local_storage = Storage()
session_storage = Storage() 