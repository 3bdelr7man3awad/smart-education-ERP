import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { createTheme } from '@mui/material/styles';
import { Provider } from 'react-redux';
import { store } from './store';

// Layout
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';

// Pages
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import PasswordReset from './pages/PasswordReset';
import Students from './pages/Students';
import Courses from './pages/Courses';
import Assignments from './pages/Assignments';
import Analytics from './pages/Analytics';
import { ApiTest } from './components/ApiTest';

// Create theme
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
});

function App() {
  return (
    <Provider store={store}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Router>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/password-reset" element={<PasswordReset />} />
            <Route path="/api-test" element={<ApiTest />} />
            <Route
              path="/"
              element={
                <ProtectedRoute>
                  <Layout>
                    <Routes>
                      <Route index element={<Dashboard />} />
                      <Route path="students" element={<Students />} />
                      <Route path="courses" element={<Courses />} />
                      <Route path="assignments" element={<Assignments />} />
                      <Route path="analytics" element={<Analytics />} />
                    </Routes>
                  </Layout>
                </ProtectedRoute>
              }
            />
          </Routes>
        </Router>
      </ThemeProvider>
    </Provider>
  );
}

export default App; 