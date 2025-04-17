import React, { useEffect, useState } from 'react';
import {
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Avatar,
  Typography,
  Badge,
  IconButton,
  Paper,
  Divider,
} from '@mui/material';
import { styled } from '@mui/material/styles';
import { useNavigate } from 'react-router-dom';
import { Chat as ChatIcon, Person as PersonIcon, Group as GroupIcon } from '@mui/icons-material';
import { formatDistanceToNow } from 'date-fns';
import { useChat } from '../../hooks/useChat';

const StyledListItem = styled(ListItem)(({ theme }) => ({
  '&:hover': {
    backgroundColor: theme.palette.action.hover,
    cursor: 'pointer',
  },
}));

const ChatList: React.FC = () => {
  const navigate = useNavigate();
  const { chats, unreadCounts, loading } = useChat();
  const [selectedChat, setSelectedChat] = useState<number | null>(null);

  useEffect(() => {
    if (chats.length > 0 && !selectedChat) {
      setSelectedChat(chats[0].id);
      navigate(`/chat/${chats[0].id}`);
    }
  }, [chats, selectedChat, navigate]);

  const handleChatSelect = (chatId: number) => {
    setSelectedChat(chatId);
    navigate(`/chat/${chatId}`);
  };

  if (loading) {
    return (
      <Paper sx={{ p: 2 }}>
        <Typography>Loading chats...</Typography>
      </Paper>
    );
  }

  return (
    <Paper sx={{ maxHeight: 'calc(100vh - 200px)', overflow: 'auto' }}>
      <List>
        {chats.map((chat, index) => (
          <React.Fragment key={chat.id}>
            <StyledListItem
              selected={selectedChat === chat.id}
              onClick={() => handleChatSelect(chat.id)}
            >
              <ListItemAvatar>
                <Badge
                  color="primary"
                  badgeContent={unreadCounts[chat.id] || 0}
                  invisible={!unreadCounts[chat.id]}
                >
                  <Avatar>
                    {chat.is_group ? <GroupIcon /> : <PersonIcon />}
                  </Avatar>
                </Badge>
              </ListItemAvatar>
              <ListItemText
                primary={chat.name || 'Unnamed Chat'}
                secondary={
                  <Typography
                    component="span"
                    variant="body2"
                    color="text.primary"
                  >
                    {chat.last_message?.content || 'No messages yet'}
                  </Typography>
                }
              />
              <Typography variant="caption" color="text.secondary">
                {chat.last_message?.created_at
                  ? formatDistanceToNow(new Date(chat.last_message.created_at), {
                      addSuffix: true,
                    })
                  : ''}
              </Typography>
            </StyledListItem>
            {index < chats.length - 1 && <Divider />}
          </React.Fragment>
        ))}
      </List>
    </Paper>
  );
};

export default ChatList; 