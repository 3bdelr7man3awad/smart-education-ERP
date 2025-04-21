import React from 'react';
import StudyAssistant from './StudyAssistant';
import { SendMessageFunction } from '../../types/chat';

interface StudyAssistantContainerProps {
  sendMessage: SendMessageFunction;
}

const StudyAssistantContainer: React.FC<StudyAssistantContainerProps> = ({ sendMessage }) => {
  const handleSendMessage = (content: string) => {
    sendMessage(content, []);
  };

  return <StudyAssistant onSendMessage={handleSendMessage} />;
};

export default StudyAssistantContainer; 