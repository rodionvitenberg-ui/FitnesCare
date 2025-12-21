'use client';

import Link from 'next/link';
import { Instagram, Youtube, Twitter, Settings, LogOut } from 'lucide-react';
import { useState } from 'react';
import LoginModal from '@/components/auth/LoginModal';
import { useDevMode } from '@/components/providers/DevModeProvider';
import { useAuth } from '@/components/providers/AuthProvider'; // <-- 1. Импортируем хук

export default function HeaderSmall() {
  const { isDevMode, toggleDevMode } = useDevMode();
  const { user, logout } = useAuth(); // <-- 2. Достаем юзера и функцию выхода
  const [isLoginOpen, setIsLoginOpen] = useState(false);

  return (
    <div className="w-full h-9 bg-[#F5F5F5] border-b border-[#E5E5E5] flex items-center justify-between px-6 sm:px-12 z-50 relative">
      
      {/* ЛЕВАЯ ЧАСТЬ */}
      <div className="flex items-center gap-4">
        <Link href="#" className="text-gray-500 hover:text-black transition"><Instagram size={14} /></Link>
        <Link href="#" className="text-gray-500 hover:text-black transition"><Youtube size={16} /></Link>
        <Link href="#" className="text-gray-500 hover:text-black transition"><Twitter size={14} /></Link>
      </div>

      {/* ПРАВАЯ ЧАСТЬ */}
      <div className="flex items-center gap-6 text-[11px] font-bold uppercase tracking-wide text-black">
        
        {/* Тумблер DevMode - ПОКАЗЫВАЕМ ТОЛЬКО КОУЧУ */}
        {user?.is_coach && (
            <div 
                onClick={toggleDevMode}
                className={`flex items-center gap-2 cursor-pointer transition-colors select-none ${isDevMode ? 'text-[var(--accent)]' : 'text-gray-400 hover:text-black'}`}
            >
                <Settings size={12} className={isDevMode ? "animate-spin-slow" : ""} />
                <span>Developer Mode: {isDevMode ? 'ON' : 'OFF'}</span>
            </div>
        )}

        {/* Разделитель показываем, только если DevMode виден */}
        {user?.is_coach && <div className="w-px h-3 bg-gray-300"></div>}

        <Link href="/help" className="hover:opacity-70">Help</Link>
        <div className="w-px h-3 bg-gray-300"></div>
        <Link href="/about" className="hover:opacity-70">About Us</Link>
        <div className="w-px h-3 bg-gray-300"></div>

        {/* ЛОГИКА ВХОДА / ВЫХОДА */}
        {user ? (
            // Если вошли - показываем "Sign Out" и, возможно, имя
            <button 
               onClick={logout} 
               className="hover:text-red-600 transition flex items-center gap-1"
            >
               <span>Sign Out ({user.username})</span>
            </button>
        ) : (
            // Если не вошли - показываем "Sign In"
            <button 
               onClick={() => setIsLoginOpen(true)} 
               className="hover:opacity-70 text-left"
            >
               Sign In
            </button>
        )}
      </div>

      <LoginModal 
        isOpen={isLoginOpen} 
        onClose={() => setIsLoginOpen(false)} 
        onSuccess={() => {
            // Модалка закрывается сама, а обновление стейта произойдет внутри LoginModal через auth.login()
            setIsLoginOpen(false);
        }} 
      />
    </div>
  );
}