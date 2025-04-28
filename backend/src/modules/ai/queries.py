import os
import json
import httpx
import strawberry
from typing import List, Optional
from .schemas import (
    AIProviderStatus,
    AICertification,
    CertificationResponse,
    AISkillset,
    SkillsetResponse,
    QuizQuestion,
    QuizResponse,
    OpenRouterModel,
    OpenRouterModelPricing,
    OpenRouterModelsResponse
)

@strawberry.type
class AIQueries:
    @strawberry.field
    async def test_deepseek_connection(self) -> AIProviderStatus:
        """Test connection to DeepSeek's API"""
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            return AIProviderStatus(
                status="error",
                provider="DeepSeek",
                message=None,
                error="DEEPSEEK_API_KEY environment variable not set",
                model="deepseek-chat"
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
                        "max_tokens": 15
                    },
                    timeout=10.0
                )
                
                response.raise_for_status()
                data = response.json()
                
                return AIProviderStatus(
                    status="success",
                    provider="DeepSeek",
                    message=data["choices"][0]["message"]["content"],
                    error=None,
                    model="deepseek-chat"
                )
                
        except httpx.HTTPStatusError as e:
            return AIProviderStatus(
                status="error",
                provider="DeepSeek",
                message=None,
                error=f"HTTP error occurred: {str(e.response.text)}",
                model="deepseek-chat"
            )
        except httpx.RequestError as e:
            return AIProviderStatus(
                status="error",
                provider="DeepSeek",
                message=None,
                error=f"Request error occurred: {str(e)}",
                model="deepseek-chat"
            )
        except Exception as e:
            return AIProviderStatus(
                status="error",
                provider="DeepSeek",
                message=None,
                error=f"Unexpected error: {str(e)}",
                model="deepseek-chat"
            )

    @strawberry.field
    async def generate_certifications_per_product(self, product: str) -> CertificationResponse:
        """Generate a list of common certifications for a given product"""
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            return CertificationResponse(
                status="error",
                certifications=[],
                error="OPENROUTER_API_KEY environment variable not set"
            )

        prompt = f"""
        List the 5 most common and recent professional certifications for {product}.
        Format the response as a JSON array with objects containing 'certificationName' and 'certificationShortName'.
        Example format:
        [
            {{"certificationName": "AWS Solutions Architect Associate", "certificationShortName": "SAA-C03"}},
            ...
        ]
        Only return the JSON array, no other text.
        The response MUST be valid JSON that can be parsed with json.loads().
        """

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://scp.samana.cloud",  # Required for OpenRouter
                        "X-Title": "Samana Cloud",  # Required for OpenRouter
                    },
                    json={
                        "model": "google/gemini-flash-1.5-8b-exp",
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.7,
                        "max_tokens": 1000
                    },
                    timeout=30.0
                )
                
                response.raise_for_status()
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                
                # Clean up the response to ensure it's valid JSON
                # Remove any markdown code block markers
                content = content.replace("```json", "").replace("```", "").strip()
                
                # Find the first '[' and the last ']' to extract just the JSON array
                start_idx = content.find('[')
                end_idx = content.rfind(']') + 1
                
                if start_idx != -1 and end_idx != 0:
                    content = content[start_idx:end_idx]
                
                # Parse the JSON response into Certification objects
                try:
                    certifications_data = json.loads(content)
                    certifications = [
                        AICertification(
                            certificationName=cert["certificationName"],
                            certificationShortName=cert["certificationShortName"]
                        )
                        for cert in certifications_data
                    ]
                    
                    return CertificationResponse(
                        status="success",
                        certifications=certifications,
                        error=None
                    )
                except json.JSONDecodeError as e:
                    return CertificationResponse(
                        status="error",
                        certifications=[],
                        error=f"Failed to parse AI response: {str(e)}\nRaw content: {content[:100]}..."
                    )
                
        except Exception as e:
            return CertificationResponse(
                status="error",
                certifications=[],
                error=f"Error generating certifications: {str(e)}"
            )

    @strawberry.field
    async def generate_skillset_topic(self, topic: str) -> SkillsetResponse:
        """Generate a list of skillsets to evaluate for a specific topic"""
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            return SkillsetResponse(
                status="error",
                skillsets=[],
                error="OPENROUTER_API_KEY environment variable not set"
            )

        prompt = f"""
        Generate 10 specific skillsets that should be evaluated during an interview for the topic: {topic}.
        Format the response as a JSON array with objects containing 'name' and 'description'.
        Each description should be a brief explanation of what to evaluate.
        Example format:
        [
            {{
                "name": "Verbal Comprehension",
                "description": "Ability to understand and process spoken information, including complex instructions and nuanced conversations"
            }},
            ...
        ]
        Only return the JSON array, no other text.
        Make sure the skillsets are specific and measurable during an interview process.
        The response MUST be valid JSON that can be parsed with json.loads().
        """

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://scp.samana.cloud",  # Required for OpenRouter
                        "X-Title": "Samana Cloud",  # Required for OpenRouter
                    },
                    json={
                        "model": "google/gemini-flash-1.5-8b-exp",
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.7,
                        "max_tokens": 1000
                    },
                    timeout=30.0
                )
                
                response.raise_for_status()
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                
                # Clean up the response to ensure it's valid JSON
                # Remove any markdown code block markers
                content = content.replace("```json", "").replace("```", "").strip()
                
                # Find the first '[' and the last ']' to extract just the JSON array
                start_idx = content.find('[')
                end_idx = content.rfind(']') + 1
                
                if start_idx != -1 and end_idx != 0:
                    content = content[start_idx:end_idx]
                
                # Parse the JSON response into Skillset objects
                try:
                    skillsets_data = json.loads(content)
                    skillsets = [
                        AISkillset(
                            name=skillset["name"],
                            description=skillset["description"]
                        )
                        for skillset in skillsets_data
                    ]
                    
                    return SkillsetResponse(
                        status="success",
                        skillsets=skillsets,
                        error=None
                    )
                except json.JSONDecodeError as e:
                    return SkillsetResponse(
                        status="error",
                        skillsets=[],
                        error=f"Failed to parse AI response: {str(e)}\nRaw content: {content[:100]}..."
                    )
                
        except Exception as e:
            return SkillsetResponse(
                status="error",
                skillsets=[],
                error=f"Error generating skillsets: {str(e)}"
            )

    @strawberry.field
    async def generate_quiz_by_topic(self, topic: str, model: str = "google/gemini-flash-1.5-8b-exp") -> QuizResponse:
        """Generate a quiz with 10 questions (2 hard, 4 easy, 4 medium) for a specific topic using OpenRouter"""
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            return QuizResponse(
                status="error",
                error="OPENROUTER_API_KEY environment variable not set"
            )

        prompt = f"""
        Generate a quiz with a random number (between 5 and 10) of questions about {topic}. Return a JSON object with a "questions" array containing the quiz questions.

        Each question in the questions array should have:
        - question: The question text
        - answers: Array of the possible answers (all should be technically correct but only one is the best for this specific question)
        - correctAnswer: The best answer for this question (must be one of the answers)
        - difficulty: The difficulty level ("easy", "medium", or "hard")

        Distribution:
        - 15% hard questions
        - 50% easy questions
        - 35% medium questions

        Example format:
        {{
            "questions": [
                {{
                    "question": "What is the primary purpose of Docker containers?",
                    "answers": [
                        "To isolate applications and their dependencies",
                        "To reduce storage space usage",
                        "To improve network security",
                        "To manage cloud resources",
                        "To automate code deployment"
                    ],
                    "correctAnswer": "To isolate applications and their dependencies",
                    "difficulty": "easy"
                }}
            ]
        }}

        Important:
        1. Make sure to return ONLY the JSON object with the questions array
        2. Ensure the response is valid JSON
        3. Each question MUST have exactly 5 answers
        4. The correctAnswer MUST be one of the answers in the answers array
        5. Difficulty MUST be one of: "easy", "medium", "hard"
        6. Use camelCase for JSON property names (correctAnswer, not correct_answer)
        The response MUST be valid JSON that can be parsed with json.loads().
        """

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://scp.samana.cloud",  # Required for OpenRouter
                        "X-Title": "Samana Cloud",  # Required for OpenRouter
                    },
                    json={
                        "model": model,  # Use the provided model
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.7,
                        "max_tokens": 4000,
                        "response_format": { "type": "json_object" }  # Request JSON format
                    },
                    timeout=45.0
                )

                response.raise_for_status()
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                
                print(f"AI Response Content: {content}")  # Debug log
                
                # Try to clean the response if it's not pure JSON
                content = content.strip()
                if content.startswith('```json'):
                    content = content.split('```json')[1]
                if content.endswith('```'):
                    content = content.split('```')[0]
                content = content.strip()
                
                # Parse the JSON response into Quiz objects
                try:
                    response_data = json.loads(content)
                    
                    # Ensure we got an object with a questions array
                    if not isinstance(response_data, dict) or "questions" not in response_data:
                        return QuizResponse(
                            status="error",
                            error="Invalid response format: expected an object with a questions array"
                        )
                    
                    questions_data = response_data["questions"]
                    if not isinstance(questions_data, list):
                        return QuizResponse(
                            status="error",
                            error="Invalid response format: questions must be an array"
                        )
                    
                    # Validate each question
                    validated_questions = []
                    for q in questions_data:
                        if not all(k in q for k in ["question", "answers", "correctAnswer", "difficulty"]):
                            continue
                        if len(q["answers"]) != 5:
                            continue
                        if q["correctAnswer"] not in q["answers"]:
                            continue
                        if q["difficulty"].lower() not in ["easy", "medium", "hard"]:
                            continue
                        validated_questions.append(q)
                    
                    if not validated_questions:
                        return QuizResponse(
                            status="error",
                            error="No valid questions in the response"
                        )
                    
                    questions = [
                        QuizQuestion(
                            question=q["question"],
                            answers=q["answers"],
                            correctAnswer=q["correctAnswer"],
                            difficulty=q["difficulty"].lower()
                        )
                        for q in validated_questions
                    ]
                    
                    return QuizResponse(
                        status="success",
                        questions=questions,
                        error=None
                    )
                except json.JSONDecodeError as e:
                    print(f"JSON Parse Error: {str(e)}")  # Debug log
                    return QuizResponse(
                        status="error",
                        error=f"Failed to parse AI response: {str(e)}"
                    )
                
        except Exception as e:
            print(f"Generation Error: {str(e)}")  # Debug log
            return QuizResponse(
                status="error",
                error=f"Error generating quiz: {str(e)}"
            )

    @strawberry.field
    async def get_openrouter_models(self) -> OpenRouterModelsResponse:
        """Get available models from OpenRouter API"""
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            return OpenRouterModelsResponse(
                status="error",
                data=None,
                error="OPENROUTER_API_KEY environment variable not set"
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
                models = []
                for model_data in data.get("data", []):
                    models.append(OpenRouterModel(
                        id=model_data.get("id", ""),
                        name=model_data.get("name", ""),
                        description=model_data.get("description", ""),
                        contextLength=model_data.get("context_length", 0),
                        pricing=OpenRouterModelPricing(
                            prompt=model_data.get("pricing", {}).get("prompt"),
                            completion=model_data.get("pricing", {}).get("completion"),
                            image=model_data.get("pricing", {}).get("image"),
                            request=model_data.get("pricing", {}).get("request")
                        ) if model_data.get("pricing") else None
                    ))
                return OpenRouterModelsResponse(
                    status="success",
                    data=models,
                    error=None
                )
        except Exception as e:
            return OpenRouterModelsResponse(
                status="error",
                data=None,
                error=f"Error fetching models: {str(e)}"
            ) 