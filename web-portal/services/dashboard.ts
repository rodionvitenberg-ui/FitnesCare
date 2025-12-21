// services/dashboard.ts

export interface Client {
    id: number;
    name: string;
    email: string;
    avatar: string; // URL картинки
    status: 'active' | 'pending' | 'finished';
    program: string;
    progress: number; // 0-100
    lastActivity: string;
  }
  
  export const mockClients: Client[] = [
    {
      id: 1,
      name: 'Алексей Смирнов',
      email: 'alex.smir@gmail.com',
      avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&h=400&fit=crop',
      status: 'active',
      program: 'Набор массы / Pro',
      progress: 75,
      lastActivity: '2 ч. назад',
    },
    {
      id: 2,
      name: 'Мария Иванова',
      email: 'maria.iva@ya.ru',
      avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=400&h=400&fit=crop',
      status: 'active',
      program: 'Похудение / Light',
      progress: 30,
      lastActivity: '5 мин. назад',
    },
    {
      id: 3,
      name: 'Дмитрий Волков',
      email: 'dim.wolf@mail.ru',
      avatar: 'https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?w=400&h=400&fit=crop',
      status: 'pending',
      program: 'Ожидает назначения',
      progress: 0,
      lastActivity: '1 дн. назад',
    },
    {
      id: 4,
      name: 'Елена Соколова',
      email: 'elena.s@gmail.com',
      avatar: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=400&h=400&fit=crop',
      status: 'finished',
      program: 'Сушка / Hard',
      progress: 100,
      lastActivity: '3 дн. назад',
    },
    // Генерируем еще парочку для массовки
    ...Array.from({ length: 6 }).map((_, i) => ({
      id: 5 + i,
      name: `Клиент ${i + 5}`,
      email: `user${i}@test.com`,
      avatar: `https://i.pravatar.cc/150?u=${i + 5}`,
      status: 'active' as const,
      program: 'Общая подготовка',
      progress: Math.floor(Math.random() * 100),
      lastActivity: 'Недавно',
    })),
  ];
  
  export const getClients = async (): Promise<Client[]> => {
    // Имитация задержки сети
    return new Promise((resolve) => {
      setTimeout(() => resolve(mockClients), 500);
    });
  };