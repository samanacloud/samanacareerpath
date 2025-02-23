import os
from openai import OpenAI
import requests

def test_openai():
    """Test OpenAI API connection"""
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # CORRECT MODEL NAME
            messages=[{"role": "user", "content": "Test connection"}],
            max_tokens=5
        )
        return {"status": "success", "error": None}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def test_deepseek():
    """Test DeepSeek API connection"""
    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",  # CONFIRMED WORKING MODEL
                "messages": [{"role": "user", "content": "Test connection"}],
                "temperature": 0.7,
                "max_tokens": 5
            }
        )
        response.raise_for_status()
        return {"status": "success", "error": None}
    except requests.exceptions.HTTPError as e:
        # Get more detailed error message
        error_msg = f"{str(e)}. Response: {e.response.text}"
        return {"status": "error", "error": error_msg}
    except Exception as e:
        return {"status": "error", "error": str(e)}