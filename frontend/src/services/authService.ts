import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL;

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

class AuthService {
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const response = await axios.post(`${API_URL}/auth/login`, credentials);
    if (response.data.access_token) {
      localStorage.setItem('user', JSON.stringify(response.data));
    }
    return response.data;
  }

  logout(): void {
    localStorage.removeItem('user');
  }

  getCurrentUser(): any {
    const userStr = localStorage.getItem('user');
    if (userStr) return JSON.parse(userStr);
    return null;
  }

  getAuthHeader(): { Authorization: string } | {} {
    const user = this.getCurrentUser();
    if (user && user.access_token) {
      return { Authorization: `Bearer ${user.access_token}` };
    }
    return {};
  }
}

export default new AuthService(); 