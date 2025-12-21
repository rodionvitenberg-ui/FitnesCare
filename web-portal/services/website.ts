// services/website.ts

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
const API_URL = `${API_BASE}/api/website`;

export interface CarouselSlide {
  id: number;
  slot_id: number;
  is_active: boolean;
  media: string | null;     // Ссылка на файл
  media_type: 'image' | 'video';
  headline: string;
  subheadline: string;
  button_count: 0 | 1 | 2;
  
  btn1_text: string;
  btn1_link: string;
  btn1_style: 'white' | 'outline';
  
  btn2_text: string;
  btn2_link: string;
  btn2_style: 'white' | 'outline';
}

// Получить все 5 слотов
export const fetchSlides = async (): Promise<CarouselSlide[]> => {
  const res = await fetch(`${API_URL}/carousel/`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to fetch slides');
  return res.json();
};

// Обновить конкретный слот
export const updateSlide = async (slotId: number, formData: FormData, token: string) => {
  const res = await fetch(`${API_URL}/carousel/${slotId}/`, {
    method: 'PATCH',
    headers: {
      'Authorization': `Bearer ${token}`,
      // Content-Type не нужен, браузер сам поставит multipart/form-data
    },
    body: formData,
  });
  if (!res.ok) throw new Error('Failed to update slide');
  return res.json();
};