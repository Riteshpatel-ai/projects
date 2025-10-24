/**
 * User Type Definitions
 */

export interface User {
  id: string;
  email: string;
  full_name?: string;
  is_active: boolean;
  is_admin?: boolean;
  created_at?: string;
  last_login?: string;
}

export interface LoginCredentials {
  username: string; // email
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  full_name?: string;
}

export interface AuthToken {
  access_token: string;
  token_type: string;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}
