'use client';

import React, { useState, useEffect } from 'react';
import { X, Upload, Save, Check, Type, MousePointer2 } from 'lucide-react';
import { CarouselSlide, updateSlide } from '@/services/website';

interface Props {
  isOpen: boolean;
  onClose: () => void;
  slides: CarouselSlide[];
  onSuccess: () => void;
}

export default function CarouselEditModal({ isOpen, onClose, slides, onSuccess }: Props) {
  const [selectedSlot, setSelectedSlot] = useState<number>(1);
  const [formData, setFormData] = useState<Partial<CarouselSlide>>({});
  const [file, setFile] = useState<File | null>(null);
  const [isSaving, setIsSaving] = useState(false);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  useEffect(() => {
    const slide = slides.find(s => s.slot_id === selectedSlot);
    if (slide) {
      setFormData(slide);
      setFile(null);
      setPreviewUrl(null);
    }
  }, [selectedSlot, slides, isOpen]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
        const f = e.target.files[0];
        setFile(f);
        setPreviewUrl(URL.createObjectURL(f));
    }
  };

  const handleSave = async () => {
    try {
      setIsSaving(true);
      const token = localStorage.getItem('access_token');
      const data = new FormData();
      Object.keys(formData).forEach(key => {
        const value = (formData as any)[key];
        if (value !== null && value !== undefined && key !== 'media') {
            data.append(key, value.toString());
        }
      });
      if (file) data.append('media', file);

      await updateSlide(selectedSlot, data, token || '');
      onSuccess();
      onClose();
    } catch (e) {
      console.error(e);
      alert('Ошибка сохранения.');
    } finally {
      setIsSaving(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[9999] flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-black/60 backdrop-blur-xl animate-fade-in" onClick={onClose} />
      <div className="relative z-50 bg-white w-full max-w-[750px] aspect-square rounded-[40px] shadow-2xl flex flex-col overflow-hidden animate-scale-up">
        
        {/* HEADER */}
        <div className="flex items-center justify-between px-10 py-8 border-b border-gray-100 flex-shrink-0 bg-white">
          <div>
            <h2 className="text-3xl font-black italic uppercase tracking-tighter">Настройка</h2>
            <p className="text-xs text-gray-400 font-bold uppercase tracking-widest mt-1">Витрина / Слот {selectedSlot}</p>
          </div>
          <button onClick={onClose} className="p-3 bg-gray-100 rounded-full hover:bg-gray-200 transition text-gray-600"><X size={24} /></button>
        </div>

        {/* BODY */}
        <div className="flex-1 overflow-y-auto p-10 space-y-10 custom-scrollbar bg-white">
            
            {/* 1. СЛОТЫ */}
            <div className="grid grid-cols-5 gap-3">
                {[1, 2, 3, 4, 5].map(num => (
                    <button
                        key={num}
                        onClick={() => setSelectedSlot(num)}
                        className={`h-16 rounded-2xl font-black text-xl transition border-2 ${
                            selectedSlot === num ? 'bg-black text-white border-black scale-105 shadow-lg' : 'bg-gray-50 text-gray-300 border-transparent hover:border-gray-200'
                        }`}
                    >
                        {num}
                    </button>
                ))}
            </div>

            {/* 2. АКТИВНОСТЬ */}
            <button 
                onClick={() => setFormData({...formData, is_active: !formData.is_active})}
                className={`w-full p-5 rounded-2xl border-2 flex items-center gap-4 transition ${formData.is_active ? 'border-black bg-black text-white' : 'border-gray-100 bg-gray-50 text-gray-400'}`}
            >
                <div className={`w-6 h-6 rounded-full flex items-center justify-center ${formData.is_active ? 'bg-white text-black' : 'bg-gray-200 text-gray-400'}`}><Check size={14} strokeWidth={4} /></div>
                <span className="font-black uppercase tracking-widest text-xs">Включить в ротацию</span>
            </button>

            {/* 3. МЕДИА */}
            <div className="aspect-video relative rounded-3xl border-2 border-dashed border-gray-200 bg-gray-50 flex flex-col items-center justify-center overflow-hidden group hover:border-black transition">
                <input type="file" accept="image/*,video/mp4" onChange={handleFileChange} className="absolute inset-0 opacity-0 cursor-pointer z-10" />
                {previewUrl || formData.media ? (
                    <>
                         {((file?.type.startsWith('video')) || (!file && formData.media_type === 'video')) ? (
                             <video src={previewUrl || formData.media || ''} className="absolute inset-0 w-full h-full object-cover opacity-50" />
                        ) : (
                             <img src={previewUrl || formData.media || ''} className="absolute inset-0 w-full h-full object-cover opacity-50" alt="preview" />
                        )}
                        <div className="z-20 bg-white px-4 py-2 rounded-full shadow-lg flex items-center gap-2">
                           <Check size={16} className="text-green-600"/> <span className="text-xs font-bold uppercase">Файл загружен</span>
                        </div>
                    </>
                ) : (
                    <div className="text-center opacity-40 group-hover:opacity-100 transition">
                        <Upload size={32} className="mx-auto mb-2" />
                        <span className="text-[10px] font-black uppercase tracking-widest">Загрузить фото/видео</span>
                    </div>
                )}
            </div>

            {/* 4. ТЕКСТЫ */}
            <div className="space-y-4">
                <div className="space-y-2">
                    <label className="flex items-center gap-2 text-xs font-bold uppercase text-gray-400"><Type size={14}/> Заголовок (H1)</label>
                    <input type="text" value={formData.headline || ''} onChange={e => setFormData({...formData, headline: e.target.value})} className="w-full p-5 rounded-2xl bg-gray-100 border-2 border-transparent focus:border-black outline-none font-black italic text-2xl uppercase placeholder-gray-300" placeholder="JUST DO IT" />
                </div>
                <div className="space-y-2">
                    <label className="flex items-center gap-2 text-xs font-bold uppercase text-gray-400"><Type size={14}/> Подзаголовок</label>
                    <input type="text" value={formData.subheadline || ''} onChange={e => setFormData({...formData, subheadline: e.target.value})} className="w-full p-5 rounded-2xl bg-gray-100 border-2 border-transparent focus:border-black outline-none font-bold placeholder-gray-300" placeholder="..." />
                </div>
            </div>

             {/* 5. КНОПКИ (ИСПРАВЛЕННАЯ ЛОГИКА) */}
             <div className="space-y-4 pt-4 border-t border-gray-100">
                <div className="flex justify-between items-center">
                    <label className="flex items-center gap-2 text-xs font-bold uppercase text-gray-400"><MousePointer2 size={14}/> Кнопки</label>
                    <div className="flex bg-gray-100 p-1 rounded-lg">
                        {[0, 1, 2].map(c => (
                            <button key={c} onClick={() => setFormData({...formData, button_count: c as any})} className={`px-3 py-1 rounded-md text-xs font-bold transition ${formData.button_count === c ? 'bg-white shadow text-black' : 'text-gray-400'}`}>{c}</button>
                        ))}
                    </div>
                </div>

                {/* Поля для КНОПКИ №1 (показываем, если 1 или 2) */}
                {(formData.button_count || 0) >= 1 && (
                     <div className="space-y-2 animate-fade-in">
                        <label className="text-[10px] font-bold uppercase text-gray-400 ml-2">Кнопка 1 (Заливка)</label>
                        <div className="grid grid-cols-2 gap-2">
                            <input placeholder="Текст (Купить)" value={formData.btn1_text || ''} onChange={e => setFormData({...formData, btn1_text: e.target.value})} className="p-3 bg-gray-50 rounded-xl text-sm font-bold outline-none border focus:border-black"/>
                            <input placeholder="Ссылка (/shop)" value={formData.btn1_link || ''} onChange={e => setFormData({...formData, btn1_link: e.target.value})} className="p-3 bg-gray-50 rounded-xl text-sm font-mono outline-none border focus:border-black"/>
                        </div>
                     </div>
                )}

                {/* Поля для КНОПКИ №2 (показываем, только если 2) */}
                {(formData.button_count || 0) >= 2 && (
                     <div className="space-y-2 animate-fade-in">
                        <label className="text-[10px] font-bold uppercase text-gray-400 ml-2">Кнопка 2 (Контур)</label>
                        <div className="grid grid-cols-2 gap-2">
                            <input placeholder="Текст (Подробнее)" value={formData.btn2_text || ''} onChange={e => setFormData({...formData, btn2_text: e.target.value})} className="p-3 bg-gray-50 rounded-xl text-sm font-bold outline-none border focus:border-black"/>
                            <input placeholder="Ссылка (/about)" value={formData.btn2_link || ''} onChange={e => setFormData({...formData, btn2_link: e.target.value})} className="p-3 bg-gray-50 rounded-xl text-sm font-mono outline-none border focus:border-black"/>
                        </div>
                     </div>
                )}
             </div>

        </div>

        {/* FOOTER */}
        <div className="p-10 border-t border-gray-100 bg-white">
            <button 
                onClick={handleSave}
                disabled={isSaving}
                className="w-full bg-black text-white py-6 rounded-2xl font-black italic uppercase text-xl hover:bg-gray-900 transition shadow-xl disabled:opacity-50"
            >
                {isSaving ? 'Сохраняем...' : 'Сохранить изменения'}
            </button>
        </div>

      </div>
    </div>
  );
}