from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field

class QuestionRequest(BaseModel):
    question: str = Field(..., description="The question to be answered")
    context: Optional[str] = Field(None, description="Optional context to help answer the question")

class ConceptExplanationRequest(BaseModel):
    concept: str = Field(..., description="The concept to explain")
    difficulty_level: str = Field("intermediate", description="The difficulty level of the explanation (beginner, intermediate, advanced)")

class TextSummarizationRequest(BaseModel):
    text: str = Field(..., description="The text to summarize")
    max_length: int = Field(150, description="Maximum length of the summary")
    min_length: int = Field(50, description="Minimum length of the summary")

class QuizCreationRequest(BaseModel):
    content: str = Field(..., description="The study material to create questions from")
    num_questions: int = Field(5, description="Number of questions to generate")

class PerformanceAnalysisRequest(BaseModel):
    student_data: Dict[str, Any] = Field(..., description="Dictionary containing student performance data")

class StudyPathRequest(BaseModel):
    student_data: Dict[str, Any] = Field(..., description="Dictionary containing student performance data")
    course_data: Dict[str, Any] = Field(..., description="Dictionary containing course information")

class StudyAssistantResponse(BaseModel):
    success: bool = Field(..., description="Whether the request was successful")
    data: Dict[str, Any] = Field(..., description="The response data")
    message: str = Field(..., description="A message describing the result") 