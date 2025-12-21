'use client';

import React, { useState, useEffect } from 'react';
import { X, ArrowRight } from 'lucide-react';
import { loginUser } from '@/services/auth';
import { useAuth } from '@/components/providers/AuthProvider';

interface Props {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

export default function LoginModal({ isOpen, onClose, onSuccess }: Props) {
  const { login } = useAuth(); 
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [shake, setShake] = useState(false);

  // Сброс состояния при открытии
  useEffect(() => {
    if (isOpen) {
      setError('');
      setUsername('');
      setPassword('');
    }
  }, [isOpen]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      // 1. Запрос к API (получаем токены и данные пользователя)
      const data = await loginUser(username, password);
      
      // 2. Сохраняем токены в localStorage
      localStorage.setItem('access_token', data.access);
      localStorage.setItem('refresh_token', data.refresh);
      // Если нужно, сохраняем роль строкой для других нужд
      if (data.role) localStorage.setItem('user_role', data.role);

      // 3. ОБНОВЛЯЕМ ГЛОБАЛЬНЫЙ СТЕЙТ (РЕАЛЬНЫМИ ДАННЫМИ С БЭКЕНДА)
      // data.is_coach приходит из твоего нового CustomTokenObtainPairSerializer
      login(data.username, data.is_coach); 

      onSuccess();
      onClose();
    } catch (err) {
      setError('Неверные данные');
      setShake(true);
      setTimeout(() => setShake(false), 300);
    } finally {
      setIsLoading(false);
    }
  };

  const handleForgotPassword = () => {
    alert("Уведомление отправлено вашему тренеру. Он свяжется с вами для восстановления доступа.");
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[9999] flex items-center justify-center p-4">
      
      {/* 1. ФОН (Блюр) */}
      <div 
        className="absolute inset-0 bg-black/60 backdrop-blur-md animate-fade-in" 
        onClick={onClose} 
      />

      {/* 2. ОКНО */}
      <div className={`relative z-50 bg-white w-full max-w-[450px] rounded-3xl shadow-2xl flex flex-col overflow-hidden animate-scale-up ${shake ? 'animate-shake' : ''}`}>
        
        {/* Header */}
        <div className="flex justify-between items-start px-8 pt-8 pb-4">
            <h2 className="text-3xl font-black italic uppercase tracking-tighter leading-none">
                Вход<br/>в Клуб
            </h2>
            <button 
                onClick={onClose} 
                className="p-2 bg-gray-100 rounded-full hover:bg-gray-200 transition"
            >
                <X size={20} className="text-gray-500" />
            </button>
        </div>

        {/* Body */}
        <form onSubmit={handleSubmit} className="px-8 pb-8 space-y-6">
            
            {/* Inputs */}
            <div className="space-y-4 mt-2">
                <div className="space-y-1">
                    <label className="text-[10px] font-bold uppercase text-gray-400 tracking-wider ml-1">Логин / Email</label>
                    <input 
                        type="text" 
                        value={username}
                        onChange={e => setUsername(e.target.value)}
                        placeholder="username"
                        className={`w-full p-4 bg-gray-50 rounded-xl font-bold text-lg outline-none border-2 transition focus:bg-white focus:border-black placeholder-gray-300 ${error ? 'border-red-500 bg-red-50' : 'border-transparent'}`}
                    />
                </div>
                
                <div className="space-y-1">
                    <label className="text-[10px] font-bold uppercase text-gray-400 tracking-wider ml-1">Пароль</label>
                    <input 
                        type="password" 
                        value={password}
                        onChange={e => setPassword(e.target.value)}
                        placeholder="••••••••"
                        className={`w-full p-4 bg-gray-50 rounded-xl font-bold text-lg outline-none border-2 transition focus:bg-white focus:border-black placeholder-gray-300 ${error ? 'border-red-500 bg-red-50' : 'border-transparent'}`}
                    />
                </div>
            </div>

            {/* Error Message */}
            {error && (
                <div className="text-red-500 text-xs font-bold text-center uppercase tracking-wide animate-pulse">
                    {error}
                </div>
            )}

            {/* Action Buttons */}
            <div className="pt-2 space-y-4">
                <button 
                    type="submit"
                    disabled={isLoading}
                    className="w-full bg-black text-white py-5 rounded-2xl font-black uppercase text-xl hover:bg-gray-900 transition shadow-xl disabled:opacity-70 flex items-center justify-center gap-2"
                >
                    {isLoading ? 'Загрузка...' : (
                        <>Войти <ArrowRight size={20} /></>
                    )}
                </button>

                <div className="text-center">
                    <button 
                        type="button"
                        onClick={handleForgotPassword}
                        className="text-xs font-medium text-gray-400 hover:text-black transition border-b border-transparent hover:border-black pb-0.5"
                    >
                        Забыли пароль?
                    </button>
                </div>
            </div>

            {/* Disclaimer */}
            <p className="text-[10px] text-center text-gray-300 leading-tight px-4">
                Авторизуясь, вы соглашаетесь с Политикой конфиденциальности и Условиями использования.
            </p>

        </form>
      </div>
    </div>
  );
}