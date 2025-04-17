import React, { useState } from 'react';
import { Box, TextField, Button, Typography, Alert, CircularProgress } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { loginStart, loginSuccess, loginFailure } from '../store/authSlice';
import { RootState } from '../store';
import authService, { LoginCredentials } from '../services/authService';

const Login: React.FC = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { loading, error } = useSelector((state: RootState) => state.auth);
  const [credentials, setCredentials] = useState<LoginCredentials>({
    email: '',
    password: '',
  });

  const handleSubmit = async (e: { preventDefault: () => void }) => {
    e.preventDefault();
    dispatch(loginStart());
    try {
      const response = await authService.login(credentials);
      dispatch(loginSuccess(response));
      navigate('/');
    } catch (err) {
      dispatch(loginFailure('Invalid email or password'));
    }
  };

  return (
    <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
      <Box sx={{ width: 300, p: 3, boxShadow: 3, borderRadius: 2 }}>
        <Typography variant="h5" align="center" gutterBottom>
          Login
        </Typography>
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth
            label="Email"
            variant="outlined"
            value={credentials.email}
            onChange={(e) => setCredentials({ ...credentials, email: e.target.value })}
            sx={{ mb: 2 }}
            required
          />
          <TextField
            fullWidth
            label="Password"
            type="password"
            variant="outlined"
            value={credentials.password}
            onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
            sx={{ mb: 2 }}
            required
          />
          <Button
            fullWidth
            variant="contained"
            type="submit"
            disabled={loading}
            sx={{ mt: 2 }}
          >
            {loading ? <CircularProgress size={24} /> : 'Login'}
          </Button>
        </form>
      </Box>
    </Box>
  );
};

export default Login; 