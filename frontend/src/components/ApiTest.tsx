import React, { useEffect, useState } from 'react';
import { Button, Typography, Box, Alert } from '@mui/material';
import { useApi } from '../hooks/useApi';

export const ApiTest: React.FC = () => {
  const { isLoading, error, testConnection } = useApi();
  const [status, setStatus] = useState<string | null>(null);

  const handleTestConnection = async () => {
    try {
      const result = await testConnection();
      setStatus(result.status);
    } catch (err) {
      // Error is already handled by the hook
    }
  };

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h6" gutterBottom>
        API Connection Test
      </Typography>
      
      <Button 
        variant="contained" 
        onClick={handleTestConnection}
        disabled={isLoading}
        sx={{ mb: 2 }}
      >
        {isLoading ? 'Testing...' : 'Test Connection'}
      </Button>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {status && (
        <Alert severity="success" sx={{ mb: 2 }}>
          API Status: {status}
        </Alert>
      )}
    </Box>
  );
}; 