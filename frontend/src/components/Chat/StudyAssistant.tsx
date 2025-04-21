import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Grid,
  CircularProgress,
  Divider,
} from '@mui/material';
import { styled } from '@mui/material/styles';
import { Send as SendIcon } from '@mui/icons-material';
import studyAssistantService, {
  QuestionRequest,
  ConceptExplanationRequest,
  TextSummarizationRequest,
  QuizCreationRequest,
  StudyAssistantResponse,
} from '../../services/studyAssistantService';

const AssistantContainer = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(2),
  marginBottom: theme.spacing(2),
}));

const FeatureButton = styled(Button)(({ theme }) => ({
  margin: theme.spacing(1),
  minWidth: '120px',
}));

const InputContainer = styled(Box)(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  marginTop: theme.spacing(2),
}));

const ResponseContainer = styled(Box)(({ theme }) => ({
  marginTop: theme.spacing(2),
  padding: theme.spacing(2),
  backgroundColor: theme.palette.background.default,
  borderRadius: theme.spacing(1),
}));

type AssistantMode = 'qa' | 'explain' | 'summarize' | 'quiz' | null;

interface StudyAssistantProps {
  onSendMessage: {
    (content: string): void;
    (content: string, files: File[]): void;
  };
}

const StudyAssistant: React.FC<StudyAssistantProps> = ({ onSendMessage }) => {
  const [mode, setMode] = useState<AssistantMode>(null);
  const [input, setInput] = useState('');
  const [context, setContext] = useState('');
  const [difficulty, setDifficulty] = useState<'beginner' | 'intermediate' | 'advanced'>('intermediate');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<StudyAssistantResponse | null>(null);

  const handleModeSelect = (selectedMode: AssistantMode) => {
    setMode(selectedMode);
    setResponse(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || !mode) return;

    setLoading(true);
    try {
      let result: StudyAssistantResponse;

      switch (mode) {
        case 'qa':
          const qaRequest: QuestionRequest = {
            question: input,
            context: context || undefined,
          };
          result = await studyAssistantService.askQuestion(qaRequest);
          break;

        case 'explain':
          const explainRequest: ConceptExplanationRequest = {
            concept: input,
            difficulty_level: difficulty,
          };
          result = await studyAssistantService.explainConcept(explainRequest);
          break;

        case 'summarize':
          const summarizeRequest: TextSummarizationRequest = {
            text: input,
          };
          result = await studyAssistantService.summarizeText(summarizeRequest);
          break;

        case 'quiz':
          const quizRequest: QuizCreationRequest = {
            content: input,
          };
          result = await studyAssistantService.createQuiz(quizRequest);
          break;

        default:
          return;
      }

      setResponse(result);
      
      // Send the response to the chat
      if (result.success) {
        let messageContent = '';
        switch (mode) {
          case 'qa':
            messageContent = `Q: ${input}\nA: ${result.data.answer}`;
            break;
          case 'explain':
            messageContent = `Concept: ${input}\nExplanation: ${result.data.explanation}`;
            break;
          case 'summarize':
            messageContent = `Summary of: ${input.substring(0, 50)}...\n\n${result.data.summary}`;
            break;
          case 'quiz':
            messageContent = `Quiz based on: ${input.substring(0, 50)}...\n\n${result.data.quiz}`;
            break;
        }
        onSendMessage(messageContent);
      }
    } catch (error) {
      console.error('Error with study assistant:', error);
      setResponse({
        success: false,
        data: {},
        message: 'An error occurred while processing your request.',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <AssistantContainer>
      <Typography variant="h6" gutterBottom>
        AI Study Assistant
      </Typography>
      <Divider sx={{ mb: 2 }} />
      
      <Box sx={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center' }}>
        <FeatureButton
          variant={mode === 'qa' ? 'contained' : 'outlined'}
          onClick={() => handleModeSelect('qa')}
        >
          Ask Question
        </FeatureButton>
        <FeatureButton
          variant={mode === 'explain' ? 'contained' : 'outlined'}
          onClick={() => handleModeSelect('explain')}
        >
          Explain Concept
        </FeatureButton>
        <FeatureButton
          variant={mode === 'summarize' ? 'contained' : 'outlined'}
          onClick={() => handleModeSelect('summarize')}
        >
          Summarize Text
        </FeatureButton>
        <FeatureButton
          variant={mode === 'quiz' ? 'contained' : 'outlined'}
          onClick={() => handleModeSelect('quiz')}
        >
          Create Quiz
        </FeatureButton>
      </Box>

      {mode && (
        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
          {mode === 'qa' && (
            <TextField
              fullWidth
              multiline
              rows={2}
              label="Context (optional)"
              value={context}
              onChange={(e) => setContext(e.target.value)}
              margin="normal"
            />
          )}
          
          {mode === 'explain' && (
            <FormControl fullWidth margin="normal">
              <InputLabel>Difficulty Level</InputLabel>
              <Select
                value={difficulty}
                label="Difficulty Level"
                onChange={(e) => setDifficulty(e.target.value as 'beginner' | 'intermediate' | 'advanced')}
              >
                <MenuItem value="beginner">Beginner</MenuItem>
                <MenuItem value="intermediate">Intermediate</MenuItem>
                <MenuItem value="advanced">Advanced</MenuItem>
              </Select>
            </FormControl>
          )}
          
          <TextField
            fullWidth
            multiline
            rows={mode === 'summarize' || mode === 'quiz' ? 4 : 2}
            label={
              mode === 'qa'
                ? 'Your Question'
                : mode === 'explain'
                ? 'Concept to Explain'
                : mode === 'summarize'
                ? 'Text to Summarize'
                : 'Content for Quiz'
            }
            value={input}
            onChange={(e) => setInput(e.target.value)}
            margin="normal"
          />
          
          <InputContainer>
            <Button
              variant="contained"
              color="primary"
              type="submit"
              disabled={!input.trim() || loading}
              endIcon={loading ? <CircularProgress size={20} /> : <SendIcon />}
              sx={{ ml: 'auto' }}
            >
              {loading ? 'Processing...' : 'Send'}
            </Button>
          </InputContainer>
        </Box>
      )}

      {response && (
        <ResponseContainer>
          <Typography variant="subtitle1" gutterBottom>
            {response.success ? 'Response:' : 'Error:'}
          </Typography>
          <Typography variant="body1">
            {response.message}
          </Typography>
          {response.success && (
            <Box sx={{ mt: 2 }}>
              {mode === 'qa' && (
                <Typography variant="body1">{response.data.answer}</Typography>
              )}
              {mode === 'explain' && (
                <Typography variant="body1">{response.data.explanation}</Typography>
              )}
              {mode === 'summarize' && (
                <Typography variant="body1">{response.data.summary}</Typography>
              )}
              {mode === 'quiz' && (
                <Typography variant="body1" component="div" sx={{ whiteSpace: 'pre-line' }}>
                  {response.data.quiz}
                </Typography>
              )}
            </Box>
          )}
        </ResponseContainer>
      )}
    </AssistantContainer>
  );
};

export default StudyAssistant; 