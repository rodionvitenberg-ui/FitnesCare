'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { Search, Menu } from 'lucide-react';

export default function HeaderBig() {
  const [isVisible, setIsVisible] = useState(true);
  const [lastScrollY, setLastScrollY] = useState(0);


  return (
    <header 
        className={`sticky top-0 z-40 bg-white border-b border-gray-100 transition-transform duration-300 ease-in-out ${isVisible ? 'translate-y-0' : '-translate-y-full'}`}
    >
      <div className="max-w-[1920px] mx-auto px-6 sm:px-12 h-16 flex items-center justify-between">
        
        {/* 1. Logo (Left) */}
        <Link href="/" className="flex-shrink-0 z-50">
           <span className="font-black text-2xl tracking-tighter italic">
             SONO<span className="text-[var(--accent)]">.ROOM</span>
           </span>
        </Link>

        {/* 2. Navigation (Center) */}
        <nav className="hidden md:flex absolute left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2 gap-8">
            <NavLink href="/dashboard">Dashboard</NavLink>
            <NavLink href="/calendar">Task Manager</NavLink>
            <NavLink href="/knowledge">Knowledge</NavLink>
            <NavLink href="/store">Store</NavLink>
        </nav>

        {/* 3. Search and Menu */}
        <div className="flex items-center gap-4 z-50">
            {/* Search*/}
            <div className="relative group hidden sm:block">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Search size={18} className="text-black group-hover:opacity-70 transition" />
                </div>
                <input 
                    type="text" 
                    placeholder="Search" 
                    className="bg-[#F5F5F5] hover:bg-[#E5E5E5] transition text-black text-sm font-medium rounded-full py-2 pl-10 pr-4 w-[160px] focus:w-[240px] focus:outline-none focus:ring-1 focus:ring-gray-300 transition-all duration-300 placeholder-gray-500"
                />
            </div>

            {/* Mobile menu */}
            <button className="md:hidden p-2 hover:bg-gray-100 rounded-full transition">
                <Menu size={24} />
            </button>
        </div>

      </div>
    </header>
  );
}

// Компонент ссылки меню
function NavLink({ href, children }: { href: string, children: React.ReactNode }) {
    return (
        <Link 
            href={href} 
            className="text-base font-bold text-black transition relative group py-4"
        >
            {children}
            <span className="absolute bottom-2 left-0 w-full h-[2px] bg-black scale-x-0 group-hover:scale-x-100 transition-transform duration-200 origin-left" />
        </Link>
    );
}