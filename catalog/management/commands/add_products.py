from django.core.management.base import BaseCommand
from catalog.models import Category, Product

class Command(BaseCommand):
    help = 'Add products to database'

    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()

        category, _ = Category.objects.get_or_create(name='Смартфон', description='мобильный телефон (современный — как правило, с сенсорным экраном), '
                                                                        'дополненный функциональностью умного устройства, фактически всегда оснащён камерой, '
                                                                        'и также фронтальной камерой, предназначенной для осуществления видеозвонков, видеоконференций '
                                                                        'и фотографирования селфи')

        products = [
            {
                'name': 'Apple iPhone 17 Pro 256 ГБ',
                'description': 'Дисплей:6.3", 2622x1206, Super Retina XDR, 120 Гц;'
                               'Связь:3G, 4G, 5G, eSIM, Nano-SIM;'
                               'Процессор:Apple A19 Pro, 6;'
                               'Память (ОЗУ/ПЗУ):12 ГБ / 256 ГБ;'
                               'Камера:48+48+48 Мп;'
                               'Питание:3988 мА*ч (Li-Ion)',
                'category': category,
                'purchase_price': 133499
            },
            {
                'name': 'Samsung Galaxy S25 FE 512 ГБ',
                'description': 'Дисплей:6.7", 2340x1080, Dynamic AMOLED 2X, 120 Гц;'
                               'Связь:3G, 4G, 5G, eSIM, Nano-SIM;'
                               'Процессор:Samsung Exynos 2400, 10 x 3.2 ГГц;'
                               'Память (ОЗУ/ПЗУ):8 ГБ / 512 ГБ;'
                               'Камера:50+8+12 Мп;'
                               'Питание:4900 мА*ч (Li-Ion)',
                'category': category,
                'purchase_price': 54999
            },
        ]

        for product_data in products:
            product, created = Product.objects.get_or_create(**product_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added product: {product.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Product already exist: {product.name}'))