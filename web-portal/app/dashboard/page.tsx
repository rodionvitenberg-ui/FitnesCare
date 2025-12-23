'use client';

import React, { useState, useEffect, useRef } from 'react';
import HeaderSmall from '@/components/layout/HeaderSmall';
import HeaderBig from '@/components/layout/HeaderBig';
import { Search, Plus, Filter } from 'lucide-react';
import { Client, getClients } from '@/services/dashboard';
import ClientCard from '@/components/dashboard/ClientCard';
import ClientSlideOver from '@/components/dashboard/ClientSlideOver';

export default function DashboardPage() {
  const [clients, setClients] = useState<Client[]>([]);
  const [loading, setLoading] = useState(true);
  
  // Состояние: объект клиента, строка 'create' или null
  const [activeItem, setActiveItem] = useState<Client | 'create' | null>(null);

  // Ссылка на элементы карточек для авто-скролла
  const itemsRef = useRef<Map<string | number, HTMLDivElement>>(null);

  useEffect(() => {
    // Имитация загрузки
    getClients().then(data => {
        setClients(data);
        setLoading(false);
    });
  }, []);

  function getMap() {
    if (!itemsRef.current) {
      itemsRef.current = new Map();
    }
    return itemsRef.current;
  }

  // === АВТО-СКРОЛЛ ===
  useEffect(() => {
    if (activeItem && typeof activeItem !== 'string') {
      const node = getMap().get(activeItem.id);
      if (node) {
        // Увеличили задержку до 600ms, чтобы дождаться конца анимации панели (500ms)
        setTimeout(() => {
            node.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'center', // Центрируем карточку по вертикали
                inline: 'nearest' 
            });
        }, 600);
      }
    }
  }, [activeItem]);

  const isPanelOpen = activeItem !== null;

  return (
    <div className="h-screen bg-[#FAFAFA] flex flex-col overflow-hidden">
      <HeaderSmall />
      <HeaderBig />
      
      {/* TOOLBAR */}
      <div className="px-8 py-6 flex flex-wrap items-center justify-between gap-4 bg-white border-b border-gray-100 shrink-0 z-20">
        <div>
            <h1 className="text-3xl font-black italic uppercase tracking-tighter">Моя Армия</h1>
            <p className="text-sm text-gray-400 font-bold">
                {isPanelOpen 
                    ? (activeItem === 'create' ? 'Новый боец' : 'Профиль бойца') 
                    : `Активные клиенты: ${clients.filter(c => c.status === 'active').length}`
                }
            </p>
        </div>

        <div className="flex items-center gap-3">
             <div className="relative group">
                <Search size={18} className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 group-hover:text-black transition" />
                <input 
                    type="text" 
                    placeholder="Поиск..." 
                    className="pl-11 pr-4 py-3 bg-gray-50 rounded-full text-sm font-medium outline-none border border-transparent focus:bg-white focus:border-gray-200 transition w-64"
                />
             </div>
             <button className="p-3 rounded-full bg-white border border-gray-200 hover:border-black hover:bg-black hover:text-white transition">
                <Filter size={18} />
             </button>
        </div>
      </div>

      {/* MAIN CONTENT SPLIT VIEW */}
      <div className="flex-1 flex overflow-hidden relative">
          
          {/* ЛЕВАЯ ЧАСТЬ: СЕТКА */}
          <div className={`
              overflow-y-auto p-8 custom-scrollbar transition-all duration-500 ease-[cubic-bezier(0.25,0.8,0.25,1)]
              ${isPanelOpen ? 'w-1/2' : 'w-full'} 
          `}>
              {loading ? (
                  <div className="animate-pulse flex gap-4 text-gray-400">Загрузка данных...</div>
              ) : (
                  <div className={`
                      grid gap-6 transition-all duration-500
                      ${isPanelOpen 
                        ? 'grid-cols-1 xl:grid-cols-2'  // ПРИ ОТКРЫТОЙ ПАНЕЛИ: строго 2 колонки
                        : 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4' // ОБЫЧНЫЙ РЕЖИМ: до 4 колонок
                      }
                  `}>
                      {/* === GHOST CARD (ЗАГЛУШКА) === */}
                      <div 
                        onClick={() => setActiveItem('create')}
                        className={`
                            group rounded-3xl border-2 border-dashed border-gray-300 
                            flex flex-col items-center justify-center cursor-pointer 
                            bg-white/50 hover:bg-white hover:border-black hover:shadow-lg transition-all duration-300
                            p-5 h-full min-h-[240px]
                            ${activeItem === 'create' ? 'border-black ring-2 ring-black ring-offset-2 bg-gray-50' : ''}
                        `}
                      >
                        <div className={`
                            w-14 h-14 rounded-full bg-gray-100 flex items-center justify-center text-gray-400 
                            group-hover:bg-black group-hover:text-white transition-colors duration-300 shadow-sm
                            ${activeItem === 'create' ? 'bg-black text-white' : ''}
                        `}>
                            <Plus size={28} />
                        </div>
                        <span className={`
                            font-bold text-sm text-gray-500 group-hover:text-black transition-colors uppercase tracking-wide mt-4
                            ${activeItem === 'create' ? 'text-black' : ''}
                        `}>
                            Новый боец
                        </span>
                      </div>

                      {/* === ОБЫЧНЫЕ КАРТОЧКИ === */}
                      {clients.map(client => (
                          <ClientCard 
                             key={client.id} 
                             ref={(node) => {
                                 if (node) getMap().set(client.id, node);
                                 else getMap().delete(client.id);
                             }}
                             client={client} 
                             isActive={typeof activeItem === 'object' && activeItem?.id === client.id}
                             onClick={() => setActiveItem(activeItem === client ? null : client)}
                          />
                      ))}
                  </div>
              )}
          </div>

          {/* ПРАВАЯ ЧАСТЬ: ВЫДВИЖНАЯ ПАНЕЛЬ */}
          <div className={`
              bg-white border-l border-gray-100 shadow-[-20px_0_40px_rgba(0,0,0,0.05)] z-30 flex-shrink-0 relative
              transition-all duration-500 ease-[cubic-bezier(0.25,0.8,0.25,1)]
              ${isPanelOpen ? 'w-1/2 translate-x-0 opacity-100' : 'w-0 translate-x-[100px] opacity-0'}
          `}>
              <div className="w-full h-full overflow-hidden"> 
                 {activeItem === 'create' ? (
                     <div className="p-10 h-full overflow-y-auto animate-in fade-in slide-in-from-bottom-4 duration-500">
                        <h2 className="text-4xl font-black italic uppercase mb-2">Новый контракт</h2>
                        <p className="text-gray-500 mb-8">Заполните данные для создания профиля нового бойца.</p>
                        
                        <div className="h-96 bg-gray-50 rounded-3xl border-2 border-dashed border-gray-200 flex flex-col items-center justify-center text-gray-400 gap-4">
                            <Plus size={48} className="opacity-20" />
                            <span className="font-medium">Здесь будет форма создания</span>
                        </div>
                     </div>
                 ) : (
                     <ClientSlideOver 
                        client={activeItem as Client} 
                        onClose={() => setActiveItem(null)} 
                     />
                 )}
              </div>
          </div>

      </div>
    </div>
  );
}