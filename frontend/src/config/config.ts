interface Config {
  apiUrl: string;
  wsUrl: string;
  uploadUrl: string;
  defaultPageSize: number;
  dateFormat: string;
  timeFormat: string;
  maxFileSize: number;
  allowedFileTypes: string[];
}

const config: Config = {
  apiUrl: process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1',
  wsUrl: process.env.REACT_APP_WS_URL || 'ws://localhost:8000/ws',
  uploadUrl: process.env.REACT_APP_UPLOAD_URL || 'http://localhost:8000/api/v1/uploads',
  defaultPageSize: 10,
  dateFormat: 'yyyy-MM-dd',
  timeFormat: 'HH:mm',
  maxFileSize: 5 * 1024 * 1024, // 5MB
  allowedFileTypes: ['jpg', 'jpeg', 'png', 'pdf', 'doc', 'docx'],
};

export default config; 