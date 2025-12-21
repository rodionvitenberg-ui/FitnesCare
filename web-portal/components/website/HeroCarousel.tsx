'use client';

import React, { useState, useEffect, useRef } from 'react';
import Link from 'next/link';
import { Settings, Play, Pause } from 'lucide-react';
import { useDevMode } from '@/components/providers/DevModeProvider';
import { CarouselSlide, fetchSlides } from '@/services/website';
import CarouselEditModal from './CarouselEditModal';

export default function HeroCarousel() {
  const { isDevMode } = useDevMode();
  
  const [slides, setSlides] = useState<CarouselSlide[]>([]);
  const [activeSlides, setActiveSlides] = useState<CarouselSlide[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [loading, setLoading] = useState(true);

  // Модалка
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Видео контроль
  const videoRef = useRef<HTMLVideoElement>(null);
  const [isPlaying, setIsPlaying] = useState(true);

  // --- ЛОГИКА ЗАГРУЗКИ ---
  const loadData = async () => {
    try {
      const allSlides = await fetchSlides();
      setSlides(allSlides);
      const active = allSlides.filter(s => s.is_active);
      setActiveSlides(active);
      // Сброс индекса, если он вдруг вышел за границы
      if (currentIndex >= active.length) setCurrentIndex(0);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const slide = activeSlides[currentIndex];

  // --- ЛОГИКА ПЕРЕКЛЮЧЕНИЯ ---
  const handleNextSlide = () => {
    setCurrentIndex((prevIndex) => 
      prevIndex === activeSlides.length - 1 ? 0 : prevIndex + 1
    );
  };

  // 1. Таймер для КАРТИНОК (7 секунд)
  useEffect(() => {
    if (!slide || slide.media_type === 'video') return;

    const timer = setTimeout(() => {
      handleNextSlide();
    }, 7000);

    return () => clearTimeout(timer);
  }, [currentIndex, slide]); // Перезапускаем таймер при смене слайда

  // 2. Видео: играет -> меняем слайд
  useEffect(() => {
    setIsPlaying(true);
    if (videoRef.current) {
        videoRef.current.load();
        videoRef.current.play().catch(() => setIsPlaying(false));
    }
  }, [currentIndex]);

  const togglePlay = () => {
    if (!videoRef.current) return;
    if (isPlaying) videoRef.current.pause();
    else videoRef.current.play();
    setIsPlaying(!isPlaying);
  };

  // Если слайдов нет совсем
  if (!loading && activeSlides.length === 0) {
    return (
        <div className="w-full h-[80vh] bg-gray-100 flex items-center justify-center relative">
            <div className="text-center">
                <h1 className="text-4xl font-black italic text-gray-300 mb-4 uppercase">No active slides</h1>
                {isDevMode && (
                    <button 
                        onClick={() => setIsModalOpen(true)}
                        className="bg-black text-white px-6 py-2 rounded-full font-bold flex items-center gap-2 mx-auto hover:scale-105 transition"
                    >
                        <Settings size={16} /> Настроить
                    </button>
                )}
            </div>
            <CarouselEditModal 
                isOpen={isModalOpen} 
                onClose={() => setIsModalOpen(false)} 
                slides={slides} 
                onSuccess={loadData}
            />
        </div>
    );
  }

  if (loading) return <div className="w-full h-[85vh] bg-gray-100 animate-pulse" />;

  return (
    <>
      <section className="relative w-full h-[85vh] bg-black">
        
        {/* 1. МЕДИА СЛОЙ */}
        <div className="absolute inset-0 z-0 overflow-hidden">
          {slide.media_type === 'video' && slide.media ? (
              <video
                  ref={videoRef}
                  className="w-full h-full object-cover"
                  autoPlay
                  muted
                  playsInline
                  // ВАЖНО: Убрали loop, добавили onEnded
                  onEnded={handleNextSlide} 
                  src={slide.media}
              />
          ) : (
              <img 
                  src={slide.media || ''} 
                  alt="Hero"
                  className="w-full h-full object-cover"
              />
          )}
          {/* Затемнение */}
          <div className="absolute inset-0 bg-black/20" />
        </div>

        {/* 2. КОНТЕНТ СЛОЙ (ЦЕНТРОВКА) */}
        {/* Добавили justify-center и text-center */}
        <div className="absolute inset-0 z-10 flex items-center justify-center px-6 sm:px-12 text-center">
          <div className="max-w-5xl pt-20 mx-auto">
              
              <h2 className="text-white text-lg sm:text-xl font-medium tracking-[0.2em] mb-4 uppercase animate-in fade-in slide-in-from-bottom-4 duration-700">
                  {slide.subheadline}
              </h2>
              
              <h1 className="text-white text-5xl sm:text-7xl md:text-8xl font-black italic tracking-tighter leading-[0.9] mb-10 uppercase animate-in fade-in slide-in-from-bottom-8 duration-700 delay-100">
                  {slide.headline}
              </h1>

              {/* Кнопки по центру (justify-center) */}
              <div className="flex flex-wrap justify-center gap-4 animate-in fade-in slide-in-from-bottom-8 duration-700 delay-200">
                  {slide.button_count >= 1 && (
                      <Link 
                          href={slide.btn1_link}
                          className="px-10 py-4 bg-white text-black rounded-full font-bold hover:scale-105 transition min-w-[160px]"
                      >
                          {slide.btn1_text}
                      </Link>
                  )}
                   {slide.button_count >= 2 && (
                      <Link 
                          href={slide.btn2_link}
                          className="px-10 py-4 border-2 border-white text-white rounded-full font-bold hover:bg-white hover:text-black transition min-w-[160px]"
                      >
                          {slide.btn2_text}
                      </Link>
                  )}
              </div>
          </div>
        </div>

        {/* 3. УПРАВЛЕНИЕ */}
        {isDevMode && (
            <button
              onClick={() => setIsModalOpen(true)}
              className="absolute top-24 right-6 sm:right-12 z-40 bg-white/20 hover:bg-white backdrop-blur-md p-3 rounded-full text-white hover:text-black transition shadow-lg"
            >
               <Settings />
            </button>
        )}

        {slide.media_type === 'video' && (
            <button
               onClick={togglePlay}
               className="absolute bottom-8 right-6 sm:right-12 z-40 p-3 rounded-full bg-black/30 hover:bg-black/60 text-white backdrop-blur-md transition border border-white/20"
            >
               {isPlaying ? <Pause size={20} fill="currentColor" /> : <Play size={20} fill="currentColor" />}
            </button>
        )}

        {/* Индикаторы (палочки снизу) */}
        {activeSlides.length > 1 && (
          <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 flex gap-3 z-30">
              {activeSlides.map((_, idx) => (
                  <button
                      key={idx}
                      onClick={() => setCurrentIndex(idx)}
                      className={`h-1.5 rounded-full transition-all duration-300 ${
                          idx === currentIndex ? 'bg-white w-12' : 'bg-white/40 w-8 hover:bg-white'
                      }`}
                  />
              ))}
          </div>
        )}

      </section>

      {/* Модалка */}
      <CarouselEditModal 
        isOpen={isModalOpen} 
        onClose={() => setIsModalOpen(false)} 
        slides={slides} 
        onSuccess={loadData}
      />
    </>
  );
}