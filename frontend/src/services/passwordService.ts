import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

export interface ResetPasswordRequest {
  email: string;
}

export interface ResetPasswordConfirm {
  token: string;
  new_password: string;
}

class PasswordService {
  async requestReset(email: string): Promise<void> {
    await axios.post(`${API_URL}/auth/password-reset`, { email });
  }

  async confirmReset(token: string, newPassword: string): Promise<void> {
    await axios.post(`${API_URL}/auth/password-reset/confirm`, {
      token,
      new_password: newPassword,
    });
  }
}

export default new PasswordService(); 