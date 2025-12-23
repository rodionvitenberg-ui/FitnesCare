'use client';

import React, { forwardRef } from 'react';
import { Client } from '@/services/dashboard';
import { MoreHorizontal, Activity } from 'lucide-react';

interface Props {
  client: Client;
  isActive: boolean;
  onClick: () => void;
}

// Используем forwardRef, чтобы родитель мог получить доступ к DOM-элементу для авто-скролла
const ClientCard = forwardRef<HTMLDivElement, Props>(({ client, isActive, onClick }, ref) => {
  return (
    <div 
      ref={ref}
      onClick={onClick}
      className={`
        group relative p-5 rounded-3xl border-2 cursor-pointer transition-all duration-300
        hover:shadow-xl hover:-translate-y-1 flex flex-col justify-between h-full min-h-[240px]
        ${isActive 
          ? 'border-black bg-black text-white' 
          : 'border-transparent bg-white text-black shadow-sm hover:border-gray-200'
        }
      `}
    >
      {/* Header: Avatar + Status */}
      <div className="flex justify-between items-start mb-4">
        <div className="relative">
             <img 
                src={client.avatar} 
                alt={client.name} 
                className={`w-12 h-12 rounded-full object-cover border-2 ${isActive ? 'border-gray-700' : 'border-gray-100'}`}
             />
             <div className={`absolute bottom-0 right-0 w-3 h-3 rounded-full border-2 border-white 
                ${client.status === 'active' ? 'bg-green-500' : client.status === 'pending' ? 'bg-yellow-400' : 'bg-gray-400'}
             `} />
        </div>
        <button className={`p-2 rounded-full transition ${isActive ? 'hover:bg-gray-800 text-gray-400' : 'hover:bg-gray-100 text-gray-400'}`}>
            <MoreHorizontal size={20} />
        </button>
      </div>

      {/* Info */}
      <div className="space-y-1 mb-6">
        <h3 className="font-bold text-lg leading-tight truncate">{client.name}</h3>
        <p className={`text-xs font-medium uppercase tracking-wide truncate ${isActive ? 'text-gray-400' : 'text-gray-400'}`}>
            {client.program}
        </p>
      </div>

      {/* Progress Bar */}
      <div className="space-y-2 mb-4">
        <div className="flex justify-between text-[10px] font-bold uppercase tracking-wider opacity-60">
            <span>Progress</span>
            <span>{client.progress}%</span>
        </div>
        <div className={`w-full h-1.5 rounded-full ${isActive ? 'bg-gray-800' : 'bg-gray-100'}`}>
            <div 
                className={`h-full rounded-full transition-all duration-500 ${client.progress === 100 ? 'bg-[var(--accent)]' : 'bg-blue-600'}`} 
                style={{ width: `${client.progress}%` }}
            />
        </div>
      </div>

      {/* Footer info */}
      <div className={`mt-auto pt-4 border-t flex items-center gap-2 text-xs font-medium ${isActive ? 'border-gray-800 text-gray-400' : 'border-gray-50 text-gray-400'}`}>
        <Activity size={12} />
        <span>Активность: {client.lastActivity}</span>
      </div>

    </div>
  );
});

ClientCard.displayName = 'ClientCard';

export default ClientCard;