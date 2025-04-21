import { useCallback } from 'react';
import { useChat } from './useChat';

export interface SendMessageFunction {
  (content: string, files?: File[]): Promise<void>;
}

export interface StudyChatResult {
  currentChat: {
    id: number;
    name: string | null;
    is_group: boolean;
    last_message?: {
      content: string;
      created_at: string;
    };
  } | undefined;
  messages: {
    id: number;
    content: string;
    sender_id: number;
    sender_name?: string;
    is_sender: boolean;
    created_at: string;
    attachments?: {
      id: number;
      file_name: string;
      file_url: string;
    }[];
  }[];
  loading: boolean;
  sendMessage: SendMessageFunction;
  markAsRead: () => Promise<void>;
}

export const useStudyChat = (chatId?: number): StudyChatResult => {
  const chat = useChat(Number(chatId));

  const sendMessage: SendMessageFunction = useCallback(
    async (content: string, files?: File[]) => {
      await chat.sendMessage(content, files);
    },
    [chat.sendMessage]
  );

  return {
    currentChat: chat.currentChat,
    messages: chat.messages,
    loading: chat.loading,
    sendMessage,
    markAsRead: chat.markAsRead,
  };
};

export default useStudyChat; 