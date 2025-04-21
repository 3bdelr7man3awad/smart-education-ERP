import React, { useCallback } from 'react';
import StudyAssistant from './StudyAssistant';

interface StudyAssistantWrapperProps {
  sendMessage: (content: string, files?: File[]) => Promise<void>;
}

const StudyAssistantWrapper: React.FC<StudyAssistantWrapperProps> = ({ sendMessage }) => {
  const handleSendMessage = useCallback((content: string) => {
    sendMessage(content, []);
  }, [sendMessage]);

  return <StudyAssistant onSendMessage={handleSendMessage} />;
};

export default StudyAssistantWrapper; 