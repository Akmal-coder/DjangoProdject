from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='publication_status',
            field=models.CharField(
                choices=[('MOD', 'На модерации'), ('PUB', 'Опубликован'),
                        ('REJ', 'Отклонен'), ('UNP', 'Снят с публикации')],
                default='MOD',
                max_length=3,
                verbose_name='Статус публикации'
            ),
        ),
        migrations.AddField(
            model_name='product',
            name='owner',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='products',
                to=settings.AUTH_USER_MODEL,
                verbose_name='Владелец'
            ),
        ),
        migrations.AlterModelOptions(
            name='product',
            options={
                'ordering': ['category', 'name'],
                'permissions': [('can_unpublish_product', 'Может отменять публикацию продукта')],
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
            },
        ),
    ]
