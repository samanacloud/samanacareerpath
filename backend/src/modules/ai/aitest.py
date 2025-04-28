from fastapi import FastAPI, HTTPException, APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import httpx
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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


class ModelInfo(BaseModel):
    id: str
    name: Optional[str] = None
    description: Optional[str] = None
    context_length: Optional[int] = None
    pricing: Optional[Dict[str, Any]] = None

class ModelsResponse(BaseModel):
    status: str
    data: Optional[List[ModelInfo]] = None
    error: Optional[str] = None

@router.get("/openrouter-models", response_model=ModelsResponse, tags=["AI"])
async def get_openrouter_models():
    """
    Get available models from OpenRouter API.
    
    Returns:
        ModelsResponse: List of available models and their details
        
    Example curl:
    ```bash
    curl -X GET "http://localhost:8000/api/ai/openrouter-models"
    ```
    
    Example Python:
    ```python
    import requests
    
    response = requests.get("http://localhost:8000/api/ai/openrouter-models")
    print(response.json())
    ```
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OPENROUTER_API_KEY environment variable not set"
        )

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://openrouter.ai/api/v1/models",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                timeout=10.0
            )
            
            response.raise_for_status()
            data = response.json()
            
            # Extract relevant model information
            models = []
            for model_data in data.get("data", []):
                models.append(ModelInfo(
                    id=model_data.get("id", ""),
                    name=model_data.get("name", ""),
                    description=model_data.get("description", ""),
                    context_length=model_data.get("context_length", 0),
                    pricing=model_data.get("pricing", {})
                ))
            
            return ModelsResponse(
                status="success",
                data=models,
                error=None
            )
            
    except Exception as e:
        return ModelsResponse(
            status="error",
            data=None,
            error=f"Error fetching models: {str(e)}"
        )

@router.get("/check-openrouter-key", tags=["AI"])
async def check_openrouter_key():
    """
    Check if the OpenRouter API key is loaded correctly.
    
    Returns:
        dict: Status of the API key
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    return {
        "key_exists": bool(api_key),
        "key_preview": f"{api_key[:10]}..." if api_key else None
    }


class MultimodalRequest(BaseModel):
    model: str = "openai/gpt-4o"
    text: str
    image_url: Optional[str] = None

class MultimodalResponse(BaseModel):
    status: str
    provider: str = "OpenRouter"
    message: Optional[str] = None
    error: Optional[str] = None
    model: str

@router.post("/openrouter-multimodal", response_model=MultimodalResponse, tags=["AI"])
async def openrouter_multimodal(request: MultimodalRequest):
    """
    Send a multimodal request (text and optional image) to OpenRouter.
    
    Parameters:
        request (MultimodalRequest): The request containing model, text, and optional image URL
    
    Returns:
        MultimodalResponse: The response from the model
        
    Example curl:
    ```bash
    curl -X POST "http://localhost:8000/api/ai/openrouter-multimodal" \\
      -H "Content-Type: application/json" \\
      -d '{"model": "openai/gpt-4o", "text": "What is in this image?", "image_url": "https://example.com/image.jpg"}'
    ```
    
    Example Python:
    ```python
    import requests
    
    response = requests.post(
        "http://localhost:8000/api/ai/openrouter-multimodal",
        json={
            "model": "openai/gpt-4o",
            "text": "What is in this image?",
            "image_url": "https://example.com/image.jpg"
        }
    )
    print(response.json())
    ```
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OPENROUTER_API_KEY environment variable not set"
        )

    try:
        # Initialize the OpenAI client with OpenRouter base URL
        client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        
        # Prepare the content array
        content = []
        
        # Add text content
        content.append({
            "type": "text",
            "text": request.text
        })
        
        # Add image content if provided
        if request.image_url:
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": request.image_url
                }
            })
        
        # Create a completion with multimodal capabilities
        completion = await client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://scp.samana.cloud",
                "X-Title": "Samana Cloud",
            },
            model=request.model,
            messages=[
                {
                    "role": "user",
                    "content": content
                }
            ],
            max_tokens=300
        )
        
        # Extract the response
        message_content = completion.choices[0].message.content
        model_used = completion.model
        
        return MultimodalResponse(
            status="success",
            message=message_content,
            model=model_used,
            error=None
        )
        
    except Exception as e:
        error_message = str(e)
        return MultimodalResponse(
            status="error",
            message=None,
            model=request.model,
            error=f"Error: {error_message}"
        )

@router.get("/openrouter-form", response_class=HTMLResponse, tags=["AI"])
async def openrouter_form():
    """
    Serves an HTML form for testing OpenRouter models with different questions.
    """
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>OpenRouter Test</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            .form-group {
                margin-bottom: 15px;
            }
            label {
                display: block;
                margin-bottom: 5px;
                font-weight: bold;
            }
            input[type="text"], select, textarea {
                width: 100%;
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                box-sizing: border-box;
            }
            button {
                background-color: #4CAF50;
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            button:hover {
                background-color: #45a049;
            }
            .result {
                margin-top: 20px;
                padding: 15px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: #f9f9f9;
                white-space: pre-wrap;
            }
            .error {
                color: red;
            }
            .hidden {
                display: none;
            }
            .loader {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #3498db;
                border-radius: 50%;
                width: 20px;
                height: 20px;
                animation: spin 2s linear infinite;
                display: inline-block;
                margin-left: 10px;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    </head>
    <body>
        <h1>OpenRouter Test</h1>
        
        <div class="form-group">
            <label for="model">Model:</label>
            <select id="model">
                <option value="openai/gpt-3.5-turbo">GPT-3.5 Turbo</option>
                <option value="openai/gpt-4o-mini">GPT-4o Mini</option>
                <option value="openai/gpt-4o">GPT-4o</option>
                <option value="anthropic/claude-3-opus">Claude 3 Opus</option>
                <option value="anthropic/claude-3-sonnet">Claude 3 Sonnet</option>
                <option value="anthropic/claude-3-haiku">Claude 3 Haiku</option>
                <option value="meta-llama/llama-3-70b-instruct">Llama 3 70B</option>
                <option value="meta-llama/llama-3-8b-instruct">Llama 3 8B</option>
            </select>
        </div>
        
        <div class="form-group">
            <label for="question">Question:</label>
            <textarea id="question" rows="4" placeholder="Enter your question here...">What is Apple?</textarea>
        </div>
        
        <button id="submit">Submit <span id="loader" class="loader hidden"></span></button>
        
        <div id="result" class="result hidden">
            <h3>Response:</h3>
            <div id="response-text"></div>
            <p><strong>Model used:</strong> <span id="model-used"></span></p>
            <p><strong>Status:</strong> <span id="status"></span></p>
        </div>
        
        <div id="error" class="error hidden"></div>
        
        <script>
            document.getElementById('submit').addEventListener('click', async () => {
                const model = document.getElementById('model').value;
                const question = document.getElementById('question').value;
                
                document.getElementById('loader').classList.remove('hidden');
                document.getElementById('result').classList.add('hidden');
                document.getElementById('error').classList.add('hidden');
                
                try {
                    const response = await fetch(`/api/ai/test-openrouter?model=${encodeURIComponent(model)}&question=${encodeURIComponent(question)}`);
                    const data = await response.json();
                    
                    if (data.status === 'success') {
                        document.getElementById('response-text').textContent = data.message;
                        document.getElementById('model-used').textContent = data.model;
                        document.getElementById('status').textContent = data.status;
                        document.getElementById('result').classList.remove('hidden');
                    } else {
                        document.getElementById('error').textContent = data.error || 'An error occurred';
                        document.getElementById('error').classList.remove('hidden');
                    }
                } catch (error) {
                    document.getElementById('error').textContent = `Error: ${error.message}`;
                    document.getElementById('error').classList.remove('hidden');
                } finally {
                    document.getElementById('loader').classList.add('hidden');
                }
            });
        </script>
    </body>
    </html>
    """

@router.get("/openrouter-multimodal-form", response_class=HTMLResponse, tags=["AI"])
async def openrouter_multimodal_form():
    """
    Serves an HTML form for testing OpenRouter multimodal capabilities (text + image).
    """
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>OpenRouter Multimodal Test</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            .form-group {
                margin-bottom: 15px;
            }
            label {
                display: block;
                margin-bottom: 5px;
                font-weight: bold;
            }
            input[type="text"], select, textarea {
                width: 100%;
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                box-sizing: border-box;
            }
            button {
                background-color: #4CAF50;
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            button:hover {
                background-color: #45a049;
            }
            .result {
                margin-top: 20px;
                padding: 15px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: #f9f9f9;
                white-space: pre-wrap;
            }
            .error {
                color: red;
            }
            .hidden {
                display: none;
            }
            .loader {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #3498db;
                border-radius: 50%;
                width: 20px;
                height: 20px;
                animation: spin 2s linear infinite;
                display: inline-block;
                margin-left: 10px;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            .image-preview {
                max-width: 100%;
                max-height: 300px;
                margin-top: 10px;
                border: 1px solid #ddd;
                display: none;
            }
        </style>
    </head>
    <body>
        <h1>OpenRouter Multimodal Test</h1>
        
        <div class="form-group">
            <label for="model">Model:</label>
            <select id="model">
                <option value="openai/gpt-4o">GPT-4o (Vision)</option>
                <option value="anthropic/claude-3-opus">Claude 3 Opus (Vision)</option>
                <option value="anthropic/claude-3-sonnet">Claude 3 Sonnet (Vision)</option>
                <option value="anthropic/claude-3-haiku">Claude 3 Haiku (Vision)</option>
            </select>
        </div>
        
        <div class="form-group">
            <label for="text">Text Prompt:</label>
            <textarea id="text" rows="4" placeholder="Enter your prompt here...">What is in this image?</textarea>
        </div>
        
        <div class="form-group">
            <label for="image_url">Image URL:</label>
            <input type="text" id="image_url" placeholder="https://example.com/image.jpg" value="https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg">
            <button id="preview-image" style="margin-top: 5px;">Preview Image</button>
            <img id="image-preview" class="image-preview">
        </div>
        
        <button id="submit">Submit <span id="loader" class="loader hidden"></span></button>
        
        <div id="result" class="result hidden">
            <h3>Response:</h3>
            <div id="response-text"></div>
            <p><strong>Model used:</strong> <span id="model-used"></span></p>
            <p><strong>Status:</strong> <span id="status"></span></p>
        </div>
        
        <div id="error" class="error hidden"></div>
        
        <script>
            document.getElementById('preview-image').addEventListener('click', () => {
                const imageUrl = document.getElementById('image_url').value;
                const imagePreview = document.getElementById('image-preview');
                
                if (imageUrl) {
                    imagePreview.src = imageUrl;
                    imagePreview.style.display = 'block';
                    imagePreview.onerror = () => {
                        imagePreview.style.display = 'none';
                        alert('Failed to load image. Please check the URL.');
                    };
                } else {
                    alert('Please enter an image URL');
                }
            });
            
            document.getElementById('submit').addEventListener('click', async () => {
                const model = document.getElementById('model').value;
                const text = document.getElementById('text').value;
                const imageUrl = document.getElementById('image_url').value;
                
                if (!text) {
                    alert('Please enter a text prompt');
                    return;
                }
                
                document.getElementById('loader').classList.remove('hidden');
                document.getElementById('result').classList.add('hidden');
                document.getElementById('error').classList.add('hidden');
                
                try {
                    const response = await fetch('/api/ai/openrouter-multimodal', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            model: model,
                            text: text,
                            image_url: imageUrl
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (data.status === 'success') {
                        document.getElementById('response-text').textContent = data.message;
                        document.getElementById('model-used').textContent = data.model;
                        document.getElementById('status').textContent = data.status;
                        document.getElementById('result').classList.remove('hidden');
                    } else {
                        document.getElementById('error').textContent = data.error || 'An error occurred';
                        document.getElementById('error').classList.remove('hidden');
                    }
                } catch (error) {
                    document.getElementById('error').textContent = `Error: ${error.message}`;
                    document.getElementById('error').classList.remove('hidden');
                } finally {
                    document.getElementById('loader').classList.add('hidden');
                }
            });
        </script>
    </body>
    </html>
    """

@router.get("/openrouter-models-ui", response_class=HTMLResponse, tags=["AI"])
async def openrouter_models_ui():
    """
    Serves an HTML page displaying available OpenRouter models.
    """
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>OpenRouter Available Models</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 1000px;
                margin: 0 auto;
                padding: 20px;
            }
            h1 {
                color: #333;
            }
            .model-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }
            .model-card {
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 15px;
                background-color: #f9f9f9;
            }
            .model-card h3 {
                margin-top: 0;
                color: #2c3e50;
            }
            .model-id {
                font-family: monospace;
                background-color: #eee;
                padding: 5px;
                border-radius: 4px;
                font-size: 14px;
                word-break: break-all;
            }
            .model-description {
                color: #555;
                font-size: 14px;
                margin: 10px 0;
            }
            .model-context {
                font-size: 14px;
            }
            .pricing {
                font-size: 13px;
                margin-top: 10px;
            }
            .pricing-item {
                display: flex;
                justify-content: space-between;
            }
            .error {
                color: red;
                padding: 20px;
                background-color: #ffeeee;
                border-radius: 5px;
            }
            .loader {
                border: 6px solid #f3f3f3;
                border-top: 6px solid #3498db;
                border-radius: 50%;
                width: 50px;
                height: 50px;
                animation: spin 2s linear infinite;
                margin: 50px auto;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            .hidden {
                display: none;
            }
            .search-box {
                width: 100%;
                padding: 10px;
                margin-bottom: 20px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 16px;
            }
        </style>
    </head>
    <body>
        <h1>OpenRouter Available Models</h1>
        
        <input type="text" id="search" class="search-box" placeholder="Search models...">
        
        <div id="loader" class="loader"></div>
        <div id="error" class="error hidden"></div>
        <div id="models-container" class="model-grid hidden"></div>
        
        <script>
            // Fetch models when page loads
            document.addEventListener('DOMContentLoaded', fetchModels);
            
            // Search functionality
            document.getElementById('search').addEventListener('input', filterModels);
            
            let allModels = [];
            
            async function fetchModels() {
                try {
                    const response = await fetch('/api/ai/openrouter-models');
                    const data = await response.json();
                    
                    if (data.status === 'success' && data.data) {
                        allModels = data.data;
                        displayModels(allModels);
                        document.getElementById('loader').classList.add('hidden');
                        document.getElementById('models-container').classList.remove('hidden');
                    } else {
                        document.getElementById('loader').classList.add('hidden');
                        document.getElementById('error').textContent = data.error || 'Failed to load models';
                        document.getElementById('error').classList.remove('hidden');
                    }
                } catch (error) {
                    document.getElementById('loader').classList.add('hidden');
                    document.getElementById('error').textContent = `Error: ${error.message}`;
                    document.getElementById('error').classList.remove('hidden');
                }
            }
            
            function displayModels(models) {
                const container = document.getElementById('models-container');
                container.innerHTML = '';
                
                if (models.length === 0) {
                    container.innerHTML = '<p>No models found matching your search.</p>';
                    return;
                }
                
                models.forEach(model => {
                    const card = document.createElement('div');
                    card.className = 'model-card';
                    
                    // Format pricing information
                    let pricingHtml = '';
                    if (model.pricing) {
                        pricingHtml = '<div class="pricing"><strong>Pricing:</strong>';
                        if (model.pricing.prompt) {
                            pricingHtml += `<div class="pricing-item"><span>Prompt:</span> <span>$${model.pricing.prompt}/1M tokens</span></div>`;
                        }
                        if (model.pricing.completion) {
                            pricingHtml += `<div class="pricing-item"><span>Completion:</span> <span>$${model.pricing.completion}/1M tokens</span></div>`;
                        }
                        pricingHtml += '</div>';
                    }
                    
                    card.innerHTML = `
                        <h3>${model.name || 'Unnamed Model'}</h3>
                        <div class="model-id">${model.id}</div>
                        <div class="model-description">${model.description || 'No description available'}</div>
                        <div class="model-context"><strong>Context Length:</strong> ${model.context_length || 'Unknown'} tokens</div>
                        ${pricingHtml}
                    `;
                    
                    container.appendChild(card);
                });
            }
            
            function filterModels() {
                const searchTerm = document.getElementById('search').value.toLowerCase();
                
                if (!searchTerm) {
                    displayModels(allModels);
                    return;
                }
                
                const filteredModels = allModels.filter(model => 
                    (model.id && model.id.toLowerCase().includes(searchTerm)) || 
                    (model.name && model.name.toLowerCase().includes(searchTerm)) ||
                    (model.description && model.description.toLowerCase().includes(searchTerm))
                );
                
                displayModels(filteredModels);
            }
        </script>
    </body>
    </html>
    """

class OpenRouterCreditResponse(BaseModel):
    status: str
    credits: Optional[float] = None
    error: Optional[str] = None

@router.get("/openrouter-credits", response_model=OpenRouterCreditResponse, tags=["AI"])
async def get_openrouter_credits():
    """
    Get available credits from OpenRouter API.

    Returns:
        OpenRouterCreditResponse: Available credits or error message

    Example curl:
    ```bash
    curl -X GET "http://localhost:8000/api/ai/openrouter-credits"
    ```

    Example Python:
    ```python
    import requests

    response = requests.get("http://localhost:8000/api/ai/openrouter-credits")
    print(response.json())
    ```
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return OpenRouterCreditResponse(
            status="error",
            credits=None,
            error="OPENROUTER_API_KEY environment variable not set"
        )

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://openrouter.ai/api/v1/credits",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                timeout=10.0
            )

            response.raise_for_status()
            data = response.json()

            # Check for error in response (OpenRouter might return 200 OK with error message)
            if "error" in data:
                return OpenRouterCreditResponse(
                    status="error",
                    credits=None,
                    error=data["error"].get("message", "Unknown OpenRouter error")
                )

            # Extract credits (assuming it's in a field named 'credits' or 'balance')
            credits = data.get("data", {}).get("balance")  # Adjust key as needed
            if credits is None:
                return OpenRouterCreditResponse(
                    status="error",
                    credits=None,
                    error="Could not retrieve credits from OpenRouter response."
                )

            return OpenRouterCreditResponse(
                status="success",
                credits=credits,
                error=None
            )

    except httpx.HTTPStatusError as e:
        return OpenRouterCreditResponse(
            status="error",
            credits=None,
            error=f"HTTP error occurred: {str(e.response.text)}"
        )
    except httpx.RequestError as e:
        return OpenRouterCreditResponse(
            status="error",
            credits=None,
            error=f"Request error occurred: {str(e)}"
        )
    except Exception as e:
        return OpenRouterCreditResponse(
            status="error",
            credits=None,
            error=f"Unexpected error: {str(e)}"
        )




        