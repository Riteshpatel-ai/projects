/**
 * Authentication API Service
 */
import apiClient from './client';

export interface LoginCredentials {
  username: string; // email
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  full_name?: string;
}

export interface User {
  id: string;
  email: string;
  full_name?: string;
  is_active: boolean;
  gmail_access_token?: string;
}

export const authApi = {
  /**
   * Login user
   */
  login: async (credentials: LoginCredentials) => {
    // FastAPI OAuth2PasswordRequestForm expects application/x-www-form-urlencoded
    const params = new URLSearchParams();
    params.append('username', credentials.username);
    params.append('password', credentials.password);

    const response = await apiClient.post('/auth/login', params, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });

    const { access_token } = response.data;
    localStorage.setItem('access_token', access_token);
    return response.data;
  },

  /**
   * Register new user
   */
  register: async (data: RegisterData) => {
    const response = await apiClient.post('/auth/register', data);
    return response.data;
  },

  /**
   * Get current user
   */
  getCurrentUser: async (): Promise<User> => {
    const response = await apiClient.get('/auth/me');
    return response.data;
  },

  /**
   * Logout user
   */
  logout: () => {
    localStorage.removeItem('access_token');
  },

  /**
   * Get Gmail authorization URL
   */
  getGmailAuthUrl: async () => {
    const response = await apiClient.get('/auth/gmail/authorize');
    return response.data.authorization_url;
  },

  /**
   * Handle Gmail callback
   */
  handleGmailCallback: async (code: string) => {
    const response = await apiClient.get('/auth/gmail/callback', {
      params: { code },
    });
    return response.data;
  },
};
