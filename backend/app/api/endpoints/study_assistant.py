from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Body
from app.services.ai_study_assistant import AIStudyAssistant
from app.schemas.study_assistant import (
    QuestionRequest,
    ConceptExplanationRequest,
    TextSummarizationRequest,
    QuizCreationRequest,
    PerformanceAnalysisRequest,
    StudyPathRequest,
    StudyAssistantResponse
)

router = APIRouter()
study_assistant = AIStudyAssistant()

@router.post("/qa", response_model=StudyAssistantResponse)
async def ask_question(request: QuestionRequest):
    """
    Ask a question and get an instant answer.
    """
    try:
        result = await study_assistant.real_time_qa(
            question=request.question,
            context=request.context
        )
        return StudyAssistantResponse(
            success=True,
            data=result,
            message="Question answered successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/explain", response_model=StudyAssistantResponse)
async def explain_concept(request: ConceptExplanationRequest):
    """
    Get a detailed explanation of a concept at a specific difficulty level.
    """
    try:
        result = await study_assistant.explain_concept(
            concept=request.concept,
            difficulty_level=request.difficulty_level
        )
        return StudyAssistantResponse(
            success=True,
            data=result,
            message="Concept explained successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/summarize", response_model=StudyAssistantResponse)
async def summarize_text(request: TextSummarizationRequest):
    """
    Summarize a text, such as a textbook or lecture notes.
    """
    try:
        result = study_assistant.summarize_text(
            text=request.text,
            max_length=request.max_length,
            min_length=request.min_length
        )
        return StudyAssistantResponse(
            success=True,
            data=result,
            message="Text summarized successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/quiz", response_model=StudyAssistantResponse)
async def create_quiz(request: QuizCreationRequest):
    """
    Create an interactive quiz based on study materials.
    """
    try:
        result = await study_assistant.create_interactive_quiz(
            content=request.content,
            num_questions=request.num_questions
        )
        return StudyAssistantResponse(
            success=True,
            data=result,
            message="Quiz created successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-performance", response_model=StudyAssistantResponse)
async def analyze_performance(request: PerformanceAnalysisRequest):
    """
    Analyze student performance and provide feedback.
    """
    try:
        result = study_assistant.analyze_performance(
            student_data=request.student_data
        )
        return StudyAssistantResponse(
            success=True,
            data=result,
            message="Performance analyzed successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/study-path", response_model=StudyAssistantResponse)
async def create_study_path(request: StudyPathRequest):
    """
    Create a personalized study path based on student performance and course requirements.
    """
    try:
        result = study_assistant.create_personalized_study_path(
            student_data=request.student_data,
            course_data=request.course_data
        )
        return StudyAssistantResponse(
            success=True,
            data=result,
            message="Study path created successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 