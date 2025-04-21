export interface Message {
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

export interface Chat {
  id: number;
  name: string | null;
  is_group: boolean;
  last_message?: {
    content: string;
    created_at: string;
  };
}

export interface ChatResponse {
  chats: Chat[];
  unread_counts: Record<number, number>;
}

export interface SendMessageFunction {
  (content: string, files?: File[]): Promise<void>;
}

export interface StudyChatResult {
  currentChat: Chat | undefined;
  messages: Message[];
  loading: boolean;
  sendMessage: SendMessageFunction;
  markAsRead: () => Promise<void>;
} 