import { useState, useEffect, useCallback } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { io, Socket } from 'socket.io-client';
import { api } from '../services/api';

interface Chat {
  id: number;
  name: string | null;
  is_group: boolean;
  last_message?: {
    content: string;
    created_at: string;
  };
}

interface Message {
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
}

interface ChatResponse {
  chats: Chat[];
  unread_counts: Record<number, number>;
}

export const useChat = (chatId?: number) => {
  const [socket, setSocket] = useState<Socket | null>(null);
  const queryClient = useQueryClient();

  // Fetch chats
  const { data: chatData, isLoading: chatsLoading } = useQuery<ChatResponse>(
    'chats',
    async () => {
      const response = await api.get('/api/v1/chats');
      return response.data;
    }
  );

  // Fetch messages for specific chat
  const { data: messages, isLoading: messagesLoading } = useQuery<Message[]>(
    ['messages', chatId],
    async () => {
      if (!chatId) return [];
      const response = await api.get(`/api/v1/chats/${chatId}`);
      return response.data.messages;
    },
    {
      enabled: !!chatId,
    }
  );

  // Send message mutation
  const sendMessageMutation = useMutation(
    async ({ content, files }: { content: string; files?: File[] }) => {
      const formData = new FormData();
      formData.append('content', content);
      if (files) {
        files.forEach((file) => formData.append('files', file));
      }
      const response = await api.post(`/api/v1/chats/${chatId}/messages`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    },
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['messages', chatId]);
        queryClient.invalidateQueries('chats');
      },
    }
  );

  // Mark messages as read mutation
  const markAsReadMutation = useMutation(
    async () => {
      if (!chatId) return;
      await api.post(`/api/v1/chats/${chatId}/read`);
    },
    {
      onSuccess: () => {
        queryClient.invalidateQueries('chats');
      },
    }
  );

  // Socket connection
  useEffect(() => {
    const newSocket = io(process.env.REACT_APP_WS_URL || 'http://localhost:8000', {
      auth: {
        token: localStorage.getItem('token'),
      },
    });

    newSocket.on('connect', () => {
      console.log('Connected to WebSocket');
    });

    newSocket.on('new_message', (message: Message) => {
      queryClient.invalidateQueries(['messages', message.chat_id]);
      queryClient.invalidateQueries('chats');
    });

    setSocket(newSocket);

    return () => {
      newSocket.close();
    };
  }, [queryClient]);

  const sendMessage = useCallback(
    async (content: string, files?: File[]) => {
      await sendMessageMutation.mutateAsync({ content, files });
    },
    [sendMessageMutation]
  );

  const markAsRead = useCallback(async () => {
    await markAsReadMutation.mutateAsync();
  }, [markAsReadMutation]);

  return {
    chats: chatData?.chats || [],
    unreadCounts: chatData?.unread_counts || {},
    currentChat: chatData?.chats.find((chat) => chat.id === chatId),
    messages: messages || [],
    loading: chatsLoading || messagesLoading,
    sendMessage,
    markAsRead,
  };
}; 