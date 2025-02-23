import os
from typing import Dict, Any
import httpx

class AIRepository:
    def __init__(self):
        # Initialize DeepSeek client settings
        self.deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
        self.deepseek_api_url = "https://api.deepseek.com/v1/chat/completions"

    async def test_deepseek_connection(self) -> Dict[str, Any]:
        """Test DeepSeek API connectivity with correct model name"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.deepseek_api_url,
                    headers={
                        "Authorization": f"Bearer {self.deepseek_api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "deepseek-chat",
                        "messages": [{
                            "role": "user",
                            "content": "Hello! Just a quick connection test. Respond with 'OK'"
                        }],
                        "temperature": 0.7,
                        "max_tokens": 20
                    }
                )
                response.raise_for_status()
                data = response.json()
                return {
                    "status": "success",
                    "provider": "DeepSeek",
                    "message": data["choices"][0]["message"]["content"],
                    "error": None,
                    "model": "deepseek-chat"
                }
        except Exception as e:
            return {
                "status": "error",
                "provider": "DeepSeek",
                "message": None,
                "error": str(e),
                "model": "deepseek-chat"
            } 