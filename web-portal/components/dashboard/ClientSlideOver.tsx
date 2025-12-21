'use client';

import React from 'react';
import { X, MessageCircle, BarChart2, Calendar } from 'lucide-react';
import { Client } from '@/services/dashboard';

interface Props {
  client: Client | null;
  onClose: () => void;
}

export default function ClientSlideOver({ client, onClose }: Props) {
  // Если клиента нет, панель пустая (но нам важна ее ширина для анимации родителя)
  if (!client) return null;

  return (
    <div className="h-full flex flex-col bg-white border-l border-gray-100 shadow-2xl overflow-hidden">
        
        {/* Header Панели */}
        <div className="p-8 border-b border-gray-100 flex justify-between items-start bg-gray-50">
            <div className="flex gap-4">
                <img src={client.avatar} className="w-16 h-16 rounded-2xl object-cover shadow-md" alt={client.name} />
                <div>
                    <h2 className="text-2xl font-black italic uppercase leading-none mb-1">{client.name}</h2>
                    <p className="text-xs font-bold text-gray-400 uppercase tracking-widest">{client.email}</p>
                    <div className="mt-2 inline-flex items-center px-2 py-1 bg-white rounded-md text-[10px] font-bold shadow-sm border border-gray-100">
                        {client.program}
                    </div>
                </div>
            </div>
            <button onClick={onClose} className="p-2 bg-white hover:bg-gray-200 rounded-full transition shadow-sm">
                <X size={20} />
            </button>
        </div>

        {/* Тело Панели */}
        <div className="flex-1 overflow-y-auto p-8 space-y-8 custom-scrollbar">
            
            {/* Quick Actions */}
            <div className="grid grid-cols-2 gap-3">
                <button className="p-4 rounded-xl bg-black text-white flex flex-col items-center justify-center gap-2 hover:opacity-90 transition">
                    <MessageCircle size={24} />
                    <span className="text-xs font-bold uppercase">Чат</span>
                </button>
                <button className="p-4 rounded-xl bg-gray-100 text-black flex flex-col items-center justify-center gap-2 hover:bg-gray-200 transition">
                    <BarChart2 size={24} />
                    <span className="text-xs font-bold uppercase">Прогресс</span>
                </button>
            </div>

            {/* Заглушка контента */}
            <div className="space-y-4">
                <h3 className="font-bold text-lg">Заметки тренера</h3>
                <textarea 
                    className="w-full h-32 p-4 bg-gray-50 rounded-xl border-none outline-none focus:ring-2 focus:ring-black/5 resize-none text-sm"
                    placeholder="Напишите заметку о клиенте..."
                />
            </div>

            <div className="space-y-4">
                 <h3 className="font-bold text-lg">Ближайшие события</h3>
                 <div className="p-4 rounded-xl border border-gray-100 flex items-center gap-4">
                    <div className="w-10 h-10 bg-blue-50 text-blue-600 rounded-lg flex items-center justify-center">
                        <Calendar size={20} />
                    </div>
                    <div>
                        <p className="font-bold text-sm">Check-in (Замеры)</p>
                        <p className="text-xs text-gray-400">Завтра, 10:00</p>
                    </div>
                 </div>
            </div>

        </div>

        {/* Footer */}
        <div className="p-6 border-t border-gray-100 bg-white">
            <button className="w-full py-4 rounded-xl border-2 border-red-100 text-red-500 font-bold text-sm hover:bg-red-50 transition">
                Архивировать клиента
            </button>
        </div>
    </div>
  );
}