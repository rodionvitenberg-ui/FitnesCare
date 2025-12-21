'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';

// Тип данных пользователя, которые мы будем хранить
interface User {
  username: string;
  is_coach: boolean;
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  login: (username: string, is_coach: boolean) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType>({} as AuthContextType);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // При первой загрузке сайта проверяем localStorage
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    const savedUsername = localStorage.getItem('username');
    const savedRole = localStorage.getItem('is_coach');

    if (token && savedUsername) {
      setUser({
        username: savedUsername,
        is_coach: savedRole === 'true', // Превращаем строку "true" в boolean
      });
    }
    setIsLoading(false);
  }, []);

  // Функция входа (вызывается из LoginModal)
  const login = (username: string, is_coach: boolean) => {
    localStorage.setItem('username', username);
    localStorage.setItem('is_coach', String(is_coach));
    setUser({ username, is_coach });
  };

  // Функция выхода
  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('username');
    localStorage.removeItem('is_coach');
    setUser(null);
    // Можно добавить редирект на главную
    window.location.href = '/'; 
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

// Хук, чтобы использовать авторизацию в любом компоненте одной строкой
export const useAuth = () => useContext(AuthContext);