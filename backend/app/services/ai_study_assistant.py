import os
from typing import List, Dict, Any, Optional
import openai
from transformers import pipeline
import numpy as np
from sklearn.cluster import KMeans
from app.core.config import settings

# Initialize OpenAI client
openai.api_key = settings.OPENAI_API_KEY

class AIStudyAssistant:
    """
    AI-powered study assistant that provides various educational support features.
    """
    
    def __init__(self):
        # Initialize summarization model
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        
        # Initialize question answering model
        self.qa_model = pipeline("question-answering", model="deepset/roberta-base-squad2")
    
    async def real_time_qa(self, question: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Provides real-time answers to student questions.
        
        Args:
            question: The question asked by the student
            context: Optional context to help answer the question
            
        Returns:
            Dict containing the answer and additional information
        """
        try:
            # If context is provided, use the QA model
            if context:
                result = self.qa_model(question=question, context=context)
                return {
                    "answer": result["answer"],
                    "confidence": result["score"],
                    "source": "qa_model"
                }
            
            # Otherwise, use OpenAI for general Q&A
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful educational assistant. Provide clear, accurate, and concise answers to student questions."},
                    {"role": "user", "content": question}
                ],
                max_tokens=500
            )
            
            return {
                "answer": response.choices[0].message.content,
                "confidence": 1.0,
                "source": "openai"
            }
        except Exception as e:
            return {
                "answer": f"Sorry, I couldn't process your question. Error: {str(e)}",
                "confidence": 0.0,
                "source": "error"
            }
    
    async def explain_concept(self, concept: str, difficulty_level: str = "intermediate") -> Dict[str, Any]:
        """
        Provides detailed explanations of concepts at different difficulty levels.
        
        Args:
            concept: The concept to explain
            difficulty_level: The difficulty level of the explanation (beginner, intermediate, advanced)
            
        Returns:
            Dict containing the explanation and additional information
        """
        try:
            prompt = f"Explain the concept of {concept} at a {difficulty_level} level. Include examples and analogies to make it easier to understand."
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful educational assistant. Provide clear, accurate, and detailed explanations of concepts."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800
            )
            
            return {
                "explanation": response.choices[0].message.content,
                "difficulty_level": difficulty_level,
                "source": "openai"
            }
        except Exception as e:
            return {
                "explanation": f"Sorry, I couldn't explain this concept. Error: {str(e)}",
                "difficulty_level": difficulty_level,
                "source": "error"
            }
    
    def summarize_text(self, text: str, max_length: int = 150, min_length: int = 50) -> Dict[str, Any]:
        """
        Summarizes textbooks, lecture notes, and other resources.
        
        Args:
            text: The text to summarize
            max_length: Maximum length of the summary
            min_length: Minimum length of the summary
            
        Returns:
            Dict containing the summary and additional information
        """
        try:
            # Split text into chunks if it's too long
            max_chunk_length = 1024
            chunks = [text[i:i+max_chunk_length] for i in range(0, len(text), max_chunk_length)]
            
            summaries = []
            for chunk in chunks:
                result = self.summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)
                summaries.append(result[0]["summary_text"])
            
            # Combine summaries if there are multiple
            final_summary = " ".join(summaries)
            
            return {
                "summary": final_summary,
                "original_length": len(text),
                "summary_length": len(final_summary),
                "compression_ratio": len(final_summary) / len(text) if len(text) > 0 else 0,
                "source": "bart"
            }
        except Exception as e:
            return {
                "summary": f"Sorry, I couldn't summarize this text. Error: {str(e)}",
                "original_length": len(text),
                "summary_length": 0,
                "compression_ratio": 0,
                "source": "error"
            }
    
    async def create_interactive_quiz(self, content: str, num_questions: int = 5) -> Dict[str, Any]:
        """
        Creates interactive quizzes based on study materials.
        
        Args:
            content: The study material to create questions from
            num_questions: Number of questions to generate
            
        Returns:
            Dict containing the quiz questions and answers
        """
        try:
            prompt = f"Create a quiz with {num_questions} multiple-choice questions based on the following content. Include the correct answer and explanations for each question:\n\n{content}"
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful educational assistant. Create clear, accurate, and challenging quiz questions based on the provided content."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000
            )
            
            return {
                "quiz": response.choices[0].message.content,
                "num_questions": num_questions,
                "source": "openai"
            }
        except Exception as e:
            return {
                "quiz": f"Sorry, I couldn't create a quiz. Error: {str(e)}",
                "num_questions": 0,
                "source": "error"
            }
    
    def analyze_performance(self, student_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyzes student performance and provides feedback.
        
        Args:
            student_data: Dictionary containing student performance data
            
        Returns:
            Dict containing performance analysis and recommendations
        """
        try:
            # Extract relevant metrics
            grades = student_data.get("grades", [])
            attendance = student_data.get("attendance", [])
            study_time = student_data.get("study_time", [])
            
            # Calculate basic statistics
            avg_grade = np.mean(grades) if grades else 0
            attendance_rate = np.mean(attendance) if attendance else 0
            avg_study_time = np.mean(study_time) if study_time else 0
            
            # Identify strengths and weaknesses
            strengths = []
            weaknesses = []
            
            if avg_grade >= 80:
                strengths.append("Strong academic performance")
            elif avg_grade < 60:
                weaknesses.append("Academic performance needs improvement")
            
            if attendance_rate >= 0.9:
                strengths.append("Excellent attendance")
            elif attendance_rate < 0.7:
                weaknesses.append("Attendance needs improvement")
            
            if avg_study_time >= 15:
                strengths.append("Good study habits")
            elif avg_study_time < 5:
                weaknesses.append("Study time needs to be increased")
            
            # Generate recommendations
            recommendations = []
            
            if avg_grade < 70:
                recommendations.append("Consider scheduling regular tutoring sessions")
            
            if attendance_rate < 0.8:
                recommendations.append("Try to attend all classes and participate actively")
            
            if avg_study_time < 10:
                recommendations.append("Increase study time to at least 10 hours per week")
            
            return {
                "performance_summary": {
                    "average_grade": avg_grade,
                    "attendance_rate": attendance_rate,
                    "average_study_time": avg_study_time
                },
                "strengths": strengths,
                "weaknesses": weaknesses,
                "recommendations": recommendations,
                "source": "scikit-learn"
            }
        except Exception as e:
            return {
                "performance_summary": {},
                "strengths": [],
                "weaknesses": [],
                "recommendations": ["Error analyzing performance data"],
                "source": "error"
            }
    
    def create_personalized_study_path(self, student_data: Dict[str, Any], course_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a personalized study path based on student performance and course requirements.
        
        Args:
            student_data: Dictionary containing student performance data
            course_data: Dictionary containing course information
            
        Returns:
            Dict containing the personalized study path
        """
        try:
            # Extract student performance data
            grades = student_data.get("grades", {})
            topics_covered = student_data.get("topics_covered", [])
            
            # Extract course data
            course_topics = course_data.get("topics", [])
            course_difficulty = course_data.get("difficulty", {})
            
            # Identify topics that need more focus
            topics_to_focus = []
            for topic in course_topics:
                if topic not in topics_covered:
                    topics_to_focus.append(topic)
                elif topic in grades and grades[topic] < 70:
                    topics_to_focus.append(topic)
            
            # Create a study schedule
            study_schedule = []
            for topic in topics_to_focus:
                difficulty = course_difficulty.get(topic, 1)
                study_time = max(2, difficulty * 3)  # More time for difficult topics
                
                study_schedule.append({
                    "topic": topic,
                    "recommended_study_time": study_time,
                    "priority": "high" if topic in grades and grades[topic] < 60 else "medium"
                })
            
            # Sort by priority
            study_schedule.sort(key=lambda x: 0 if x["priority"] == "high" else 1)
            
            return {
                "study_schedule": study_schedule,
                "topics_to_focus": topics_to_focus,
                "estimated_completion_time": sum(item["recommended_study_time"] for item in study_schedule),
                "source": "scikit-learn"
            }
        except Exception as e:
            return {
                "study_schedule": [],
                "topics_to_focus": [],
                "estimated_completion_time": 0,
                "source": "error"
            } 