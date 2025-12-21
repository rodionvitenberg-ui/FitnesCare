// services/auth.ts
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

export interface AuthResponse {
  access: string;
  refresh: string;
  username: string;
  is_coach: boolean;
}

export const loginUser = async (username: string, password: string): Promise<AuthResponse> => {
  const res = await fetch(`${API_URL}/api/token/`, { // Стандартный путь Django SimpleJWT
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  });

  if (!res.ok) {
    throw new Error('Неверный логин или пароль');
  }

  return res.json();
};