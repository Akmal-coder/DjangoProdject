from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product

class Command(BaseCommand):
    help = 'Создает группу "Модератор продуктов" и назначает необходимые права'

    def handle(self, *args, **options):
        # 1. Получаем или создаем группу
        moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')

        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" создана.'))
        else:
            self.stdout.write(self.style.WARNING('Группа "Модератор продуктов" уже существует.'))

        # 2. Получаем ContentType для модели Product
        product_content_type = ContentType.objects.get_for_model(Product)

        # 3. Получаем нужные разрешения
        #    a) Кастомное разрешение на отмену публикации
        can_unpublish_perm, _ = Permission.objects.get_or_create(
            codename='can_unpublish_product',
            content_type=product_content_type,
        )
        #    b) Стандартное разрешение на удаление любого продукта (delete_product)
        delete_perm = Permission.objects.get(
            codename='delete_product',
            content_type=product_content_type,
        )

        # 4. Назначаем разрешения группе
        moderator_group.permissions.add(can_unpublish_perm, delete_perm)
        moderator_group.save()

        self.stdout.write(
            self.style.SUCCESS(
                f'Группе "{moderator_group.name}" назначены права: '
                f'{can_unpublish_perm.name}, {delete_perm.name}'
            )
        )