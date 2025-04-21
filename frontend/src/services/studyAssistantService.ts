import axios from 'axios';
import { API_URL } from '../config';

const STUDY_ASSISTANT_API = `${API_URL}/api/v1/study-assistant`;

export interface QuestionRequest {
  question: string;
  context?: string;
}

export interface ConceptExplanationRequest {
  concept: string;
  difficulty_level?: 'beginner' | 'intermediate' | 'advanced';
}

export interface TextSummarizationRequest {
  text: string;
  max_length?: number;
  min_length?: number;
}

export interface QuizCreationRequest {
  content: string;
  num_questions?: number;
}

export interface PerformanceAnalysisRequest {
  student_data: Record<string, any>;
}

export interface StudyPathRequest {
  student_data: Record<string, any>;
  course_data: Record<string, any>;
}

export interface StudyAssistantResponse<T = any> {
  success: boolean;
  data: T;
  message: string;
}

const studyAssistantService = {
  /**
   * Ask a question and get an instant answer
   */
  askQuestion: async (request: QuestionRequest): Promise<StudyAssistantResponse> => {
    const response = await axios.post(`${STUDY_ASSISTANT_API}/qa`, request);
    return response.data;
  },

  /**
   * Get a detailed explanation of a concept at a specific difficulty level
   */
  explainConcept: async (request: ConceptExplanationRequest): Promise<StudyAssistantResponse> => {
    const response = await axios.post(`${STUDY_ASSISTANT_API}/explain`, request);
    return response.data;
  },

  /**
   * Summarize a text, such as a textbook or lecture notes
   */
  summarizeText: async (request: TextSummarizationRequest): Promise<StudyAssistantResponse> => {
    const response = await axios.post(`${STUDY_ASSISTANT_API}/summarize`, request);
    return response.data;
  },

  /**
   * Create an interactive quiz based on study materials
   */
  createQuiz: async (request: QuizCreationRequest): Promise<StudyAssistantResponse> => {
    const response = await axios.post(`${STUDY_ASSISTANT_API}/quiz`, request);
    return response.data;
  },

  /**
   * Analyze student performance and provide feedback
   */
  analyzePerformance: async (request: PerformanceAnalysisRequest): Promise<StudyAssistantResponse> => {
    const response = await axios.post(`${STUDY_ASSISTANT_API}/analyze-performance`, request);
    return response.data;
  },

  /**
   * Create a personalized study path based on student performance and course requirements
   */
  createStudyPath: async (request: StudyPathRequest): Promise<StudyAssistantResponse> => {
    const response = await axios.post(`${STUDY_ASSISTANT_API}/study-path`, request);
    return response.data;
  },
};

export default studyAssistantService; 