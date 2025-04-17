import api from '../config/api';

// Auth endpoints
export const auth = {
  login: (email: string, password: string) => 
    api.post('/api/v1/auth/login', { email, password }),
  register: (userData: any) => 
    api.post('/api/v1/auth/register', userData),
  logout: () => {
    localStorage.removeItem('token');
  },
};

// User endpoints
export const users = {
  getCurrentUser: () => 
    api.get('/api/v1/users/me'),
  updateProfile: (userData: any) => 
    api.put('/api/v1/users/me', userData),
};

// Course endpoints
export const courses = {
  getAll: () => 
    api.get('/api/v1/courses'),
  getById: (id: string) => 
    api.get(`/api/v1/courses/${id}`),
  create: (courseData: any) => 
    api.post('/api/v1/courses', courseData),
  update: (id: string, courseData: any) => 
    api.put(`/api/v1/courses/${id}`, courseData),
  delete: (id: string) => 
    api.delete(`/api/v1/courses/${id}`),
};

// Assignment endpoints
export const assignments = {
  getAll: () => 
    api.get('/api/v1/assignments'),
  getById: (id: string) => 
    api.get(`/api/v1/assignments/${id}`),
  create: (assignmentData: any) => 
    api.post('/api/v1/assignments', assignmentData),
  update: (id: string, assignmentData: any) => 
    api.put(`/api/v1/assignments/${id}`, assignmentData),
  delete: (id: string) => 
    api.delete(`/api/v1/assignments/${id}`),
};

// Health check
export const health = {
  check: () => 
    api.get('/api/v1/health'),
}; 