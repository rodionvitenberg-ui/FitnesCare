'use client';

import React, { useState, useEffect } from 'react';
import HeaderSmall from '@/components/layout/HeaderSmall';
import HeaderBig from '@/components/layout/HeaderBig';
import { Search, Plus, Filter } from 'lucide-react';
import { Client, getClients } from '@/services/dashboard';
import ClientCard from '@/components/dashboard/ClientCard';
import ClientSlideOver from '@/components/dashboard/ClientSlideOver';

export default function DashboardPage() {
  const [clients, setClients] = useState<Client[]>([]);
  const [loading, setLoading] = useState(true);
  
  // Выбранный клиент (если есть, панель открыта)
  const [selectedClient, setSelectedClient] = useState<Client | null>(null);

  useEffect(() => {
    // Грузим моковые данные
    getClients().then(data => {
        setClients(data);
        setLoading(false);
    });
  }, []);

  return (
    <div className="h-screen bg-[#FAFAFA] flex flex-col overflow-hidden">
      <HeaderSmall />
      <HeaderBig />
      
      {/* TOOLBAR */}
      <div className="px-8 py-6 flex flex-wrap items-center justify-between gap-4 bg-white border-b border-gray-100 shrink-0 z-20">
        <div>
            <h1 className="text-3xl font-black italic uppercase tracking-tighter">Моя Армия</h1>
            <p className="text-sm text-gray-400 font-bold">Активные клиенты: {clients.filter(c => c.status === 'active').length}</p>
        </div>

        <div className="flex items-center gap-3">
             {/* Поиск */}
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

             <button className="px-6 py-3 bg-[var(--accent)] text-black rounded-full font-bold text-sm flex items-center gap-2 hover:brightness-105 transition shadow-lg shadow-[var(--accent)]/20">
                <Plus size={18} /> Новый боец
             </button>
        </div>
      </div>

      {/* MAIN CONTENT AREA (Split View) */}
      <div className="flex-1 flex overflow-hidden relative">
          
          {/* ЛЕВАЯ ЧАСТЬ: СЕТКА */}
          <div className={`
              flex-1 overflow-y-auto p-8 custom-scrollbar transition-all duration-500 ease-in-out
              ${selectedClient ? 'mr-0' : 'mr-0'} // Можно добавить отступ, если нужно
          `}>
              {loading ? (
                  <div className="animate-pulse flex gap-4">Загрузка...</div>
              ) : (
                  <div className={`
                      grid gap-6 transition-all duration-500
                      ${selectedClient 
                        ? 'grid-cols-1 md:grid-cols-2'  // Сжатый режим (2 колонки)
                        : 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4' // Полный режим
                      }
                  `}>
                      {clients.map(client => (
                          <ClientCard 
                             key={client.id} 
                             client={client} 
                             isActive={selectedClient?.id === client.id}
                             onClick={() => setSelectedClient(client.id === selectedClient?.id ? null : client)}
                          />
                      ))}
                  </div>
              )}
          </div>

          {/* ПРАВАЯ ЧАСТЬ: ВЫДВИЖНАЯ ПАНЕЛЬ */}
          {/* Мы не убираем ее из DOM, а меняем ширину, чтобы работала анимация сжатия сетки */}
          <div className={`
              bg-white shadow-2xl z-30 flex-shrink-0 transition-all duration-500 ease-[cubic-bezier(0.25,0.8,0.25,1)]
              ${selectedClient ? 'w-[450px] translate-x-0 opacity-100' : 'w-0 translate-x-[50px] opacity-0'}
          `}>
              <div className="w-[450px] h-full"> {/* Фиксированный контейнер внутри, чтобы контент не плющило при анимации */}
                 <ClientSlideOver 
                    client={selectedClient} 
                    onClose={() => setSelectedClient(null)} 
                 />
              </div>
          </div>

      </div>
    </div>
  );
}