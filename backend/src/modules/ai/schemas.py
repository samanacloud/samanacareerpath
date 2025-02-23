from typing import Optional, List
import strawberry
from dataclasses import field

@strawberry.type
class AIProviderStatus:
    status: str = strawberry.field(description="Success or error status")
    provider: str = strawberry.field(description="AI provider name")
    message: Optional[str] = strawberry.field(description="Response message if successful")
    error: Optional[str] = strawberry.field(description="Error message if failed")
    model: Optional[str] = strawberry.field(description="Model used for the test")

@strawberry.type
class AICertification:
    certificationName: str = strawberry.field(description="Full name of the certification")
    certificationShortName: str = strawberry.field(description="Short name or code of the certification")

@strawberry.type
class CertificationResponse:
    status: str = strawberry.field(description="Success or error status")
    certifications: List[AICertification] = strawberry.field(description="List of certifications")
    error: Optional[str] = strawberry.field(description="Error message if any", default=None)

@strawberry.type
class AISkillset:
    name: str = strawberry.field(description="Name of the skill to evaluate")
    description: str = strawberry.field(description="Brief description of what to evaluate")

@strawberry.type
class SkillsetResponse:
    status: str = strawberry.field(description="Success or error status")
    skillsets: List[AISkillset] = strawberry.field(description="List of skillsets to evaluate")
    error: Optional[str] = strawberry.field(description="Error message if any", default=None)

@strawberry.type
class AIConnectionTest:
    deepseek: AIProviderStatus = strawberry.field(description="DeepSeek connection status")
    all_operational: bool = strawberry.field(description="Whether all providers are operational")

@strawberry.type
class QuizQuestion:
    question: str
    answers: List[str]
    correctAnswer: str = strawberry.field(description="The correct answer for this question")
    difficulty: str

@strawberry.type
class QuizResponse:
    status: str
    error: Optional[str] = None
    questions: List[QuizQuestion] = field(default_factory=list) 