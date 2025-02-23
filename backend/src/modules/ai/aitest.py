from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from typing import Optional
import httpx
import os

router = APIRouter()

class DeepSeekResponse(BaseModel):
    status: str
    provider: str = "DeepSeek"
    message: Optional[str] = None
    error: Optional[str] = None
    model: str = "deepseek-chat"

@router.get("/test-deepseek", response_model=DeepSeekResponse, tags=["AI"])
async def test_deepseek_connection():
    """
    Test connection to DeepSeek's API.
    
    Returns:
        DeepSeekResponse: Connection test results
        
    Example curl:
    ```bash
    curl -X GET "http://localhost:8000/api/ai/test-deepseek"
    ```
    
    Example Python:
    ```python
    import requests
    
    response = requests.get("http://localhost:8000/api/ai/test-deepseek")
    print(response.json())
    ```
    """
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="DEEPSEEK_API_KEY environment variable not set"
        )

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": "Test connection"}],
                    "max_tokens": 50
                },
                timeout=10.0
            )
            
            response.raise_for_status()
            data = response.json()
            
            return DeepSeekResponse(
                status="success",
                message=data["choices"][0]["message"]["content"],
                error=None
            )
            
    except httpx.HTTPStatusError as e:
        return DeepSeekResponse(
            status="error",
            message=None,
            error=f"HTTP error occurred: {str(e.response.text)}"
        )
    except httpx.RequestError as e:
        return DeepSeekResponse(
            status="error",
            message=None,
            error=f"Request error occurred: {str(e)}"
        )
    except Exception as e:
        return DeepSeekResponse(
            status="error",
            message=None,
            error=f"Unexpected error: {str(e)}"
        ) 