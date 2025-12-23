from django.core.management.base import BaseCommand
from clients.models import Category, Attribute, Tag

class Command(BaseCommand):
    help = 'Заполняет базу начальными данными для фитнес-коуча'

    def handle(self, *args, **options):
        # 1. Категории
        categories = [
            ("fat-loss", "Похудение (Fat Loss)", "Сжигание жира, дефицит калорий"),
            ("bulking", "Набор массы (Bulking)", "Рост мышц, профицит"),
            ("recomp", "Рекомпозиция", "Жир вниз, мышцы вверх"),
            ("maintenance", "Поддержание", "Сохранение формы"),
            ("powerlifting", "Силовая подготовка", "Рост силовых показателей"),
            ("rehab", "Реабилитация", "Восстановление после травм"),
        ]
        
        for slug, name, desc in categories:
            Category.objects.get_or_create(slug=slug, defaults={'name': name, 'description': desc})
        self.stdout.write(self.style.SUCCESS(f'Создано {len(categories)} категорий.'))

        # 2. Атрибуты (Антропометрия и Силовые)
        attributes = [
            # slug, name, type
            ("weight", "Вес тела", "number"),
            ("waist", "Обхват талии", "number"),
            ("hips", "Обхват бедер", "number"),
            ("chest", "Обхват груди", "number"),
            ("biceps", "Бицепс", "number"),
            ("fat_percent", "Процент жира", "number"),
            ("bench_press", "Жим лежа (1ПМ)", "number"),
            ("squat", "Приседания", "number"),
            ("deadlift", "Становая тяга", "number"),
            ("steps", "Шаги за день", "number"),
            ("calories", "Ср. калорийность", "number"),
        ]

        for slug, name, attr_type in attributes:
            Attribute.objects.get_or_create(slug=slug, defaults={'name': name, 'attr_type': attr_type})
        self.stdout.write(self.style.SUCCESS(f'Создано {len(attributes)} атрибутов.'))

        # 3. Теги
        tags = [
            ("paid", "Оплачено", "#28a745"),       # Green
            ("overdue", "Должник", "#dc3545"),     # Red
            ("newbie", "Новичок", "#17a2b8"),      # Cyan
            ("pro", "PRO / Опытный", "#6c757d"),   # Grey
            ("injured", "Травма", "#ffc107"),      # Yellow
            ("vip", "VIP Клиент", "#6610f2"),      # Purple
            ("whiner", "Нытик", "#343a40"),        # Dark
        ]

        for slug, name, color in tags:
            Tag.objects.get_or_create(slug=slug, defaults={'name': name, 'color': color})
        self.stdout.write(self.style.SUCCESS(f'Создано {len(tags)} тегов.'))
        
        self.stdout.write(self.style.SUCCESS('--- БАЗА ДАННЫХ ГОТОВА К РАБОТЕ ---'))