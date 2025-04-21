// API configuration
export const API_URL = process.env.VITE_API_URL || 'http://localhost:8000';

// Application configuration
export const APP_NAME = 'Smart Education ERP';
export const APP_VERSION = '1.0.0';

// Feature flags
export const FEATURES = {
  AI_STUDY_ASSISTANT: true,
  REAL_TIME_CHAT: true,
  NOTIFICATIONS: true,
  DARK_MODE: true,
};

// Theme configuration
export const THEME = {
  primaryColor: '#1976d2',
  secondaryColor: '#dc004e',
  backgroundColor: '#f5f5f5',
  textColor: '#333333',
};

// Localization configuration
export const DEFAULT_LANGUAGE = 'en';
export const SUPPORTED_LANGUAGES = ['en', 'ar']; 