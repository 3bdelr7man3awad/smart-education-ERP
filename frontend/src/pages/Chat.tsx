import React from 'react';
import { Box, Grid, Paper } from '@mui/material';
import ChatList from '../components/Chat/ChatList';
import ChatWindow from '../components/Chat/ChatWindow';

const Chat: React.FC = () => {
  return (
    <Box sx={{ flexGrow: 1, height: 'calc(100vh - 64px)', p: 2 }}>
      <Grid container spacing={2} sx={{ height: '100%' }}>
        <Grid item xs={12} md={4}>
          <Paper sx={{ height: '100%' }}>
            <ChatList />
          </Paper>
        </Grid>
        <Grid item xs={12} md={8}>
          <Paper sx={{ height: '100%' }}>
            <ChatWindow />
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Chat; 