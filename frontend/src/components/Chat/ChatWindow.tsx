import React, { useEffect, useRef, useState } from 'react';
import {
  Box,
  Paper,
  TextField,
  IconButton,
  Typography,
  Avatar,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Divider,
  CircularProgress,
} from '@mui/material';
import { styled } from '@mui/material/styles';
import { Send as SendIcon, AttachFile as AttachFileIcon } from '@mui/icons-material';
import { formatDistanceToNow } from 'date-fns';
import { useParams } from 'react-router-dom';
import { useChat } from '../../hooks/useChat';

const MessageContainer = styled(Box)(({ theme }) => ({
  display: 'flex',
  flexDirection: 'column',
  height: 'calc(100vh - 200px)',
  padding: theme.spacing(2),
}));

const MessagesList = styled(List)({
  flex: 1,
  overflow: 'auto',
  padding: 0,
});

const MessageInput = styled(Box)(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  padding: theme.spacing(2),
  borderTop: `1px solid ${theme.palette.divider}`,
}));

const ChatWindow: React.FC = () => {
  const { chatId } = useParams<{ chatId: string }>();
  const { currentChat, messages, loading, sendMessage, markAsRead } = useChat(Number(chatId));
  const [newMessage, setNewMessage] = useState('');
  const [attachments, setAttachments] = useState<File[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (chatId) {
      markAsRead(Number(chatId));
    }
  }, [chatId, markAsRead]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newMessage.trim() && attachments.length === 0) return;

    await sendMessage(newMessage, attachments);
    setNewMessage('');
    setAttachments([]);
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setAttachments(Array.from(event.target.files));
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="100%">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <MessageContainer>
      <Typography variant="h6" gutterBottom>
        {currentChat?.name || 'Chat'}
      </Typography>
      <Divider />
      <MessagesList>
        {messages.map((message, index) => (
          <ListItem
            key={message.id}
            sx={{
              flexDirection: 'column',
              alignItems: message.is_sender ? 'flex-end' : 'flex-start',
            }}
          >
            <Box
              sx={{
                display: 'flex',
                alignItems: 'center',
                maxWidth: '70%',
                mb: 1,
              }}
            >
              {!message.is_sender && (
                <ListItemAvatar>
                  <Avatar>{message.sender_name?.[0] || 'U'}</Avatar>
                </ListItemAvatar>
              )}
              <Paper
                sx={{
                  p: 2,
                  bgcolor: message.is_sender ? 'primary.main' : 'grey.100',
                  color: message.is_sender ? 'white' : 'text.primary',
                }}
              >
                <ListItemText
                  primary={message.content}
                  secondary={
                    <Typography variant="caption" color="inherit">
                      {formatDistanceToNow(new Date(message.created_at), {
                        addSuffix: true,
                      })}
                    </Typography>
                  }
                />
                {message.attachments?.length > 0 && (
                  <Box mt={1}>
                    {message.attachments.map((attachment) => (
                      <Typography
                        key={attachment.id}
                        variant="caption"
                        component="div"
                      >
                        📎 {attachment.file_name}
                      </Typography>
                    ))}
                  </Box>
                )}
              </Paper>
            </Box>
          </ListItem>
        ))}
        <div ref={messagesEndRef} />
      </MessagesList>
      <MessageInput component="form" onSubmit={handleSendMessage}>
        <IconButton component="label">
          <input
            type="file"
            hidden
            multiple
            onChange={handleFileChange}
          />
          <AttachFileIcon />
        </IconButton>
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Type a message..."
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          sx={{ mx: 2 }}
        />
        <IconButton
          color="primary"
          type="submit"
          disabled={!newMessage.trim() && attachments.length === 0}
        >
          <SendIcon />
        </IconButton>
      </MessageInput>
    </MessageContainer>
  );
};

export default ChatWindow; 