import HeaderSmall from '@/components/layout/HeaderSmall';
import HeaderBig from '@/components/layout/HeaderBig';
import HeroCarousel from '@/components/website/HeroCarousel';

export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      {/* Структура навигации */}
      <HeaderSmall />
      <HeaderBig />

      {/* Hero Section (Место под карусель) */}
      <main>
        <HeroCarousel />

        {/* Секция контента (Instagram и товары) */}
        <section className="max-w-[1920px] mx-auto px-12 py-24">
            <div className="grid grid-cols-3 gap-4 h-[600px]">
                <div className="bg-[#F5F5F5] col-span-1 row-span-2"></div>
                <div className="bg-[#F5F5F5]"></div>
                <div className="bg-[#F5F5F5]"></div>
                <div className="bg-[#F5F5F5] col-span-2"></div>
            </div>
        </section>
      </main>
    </div>
  );
}