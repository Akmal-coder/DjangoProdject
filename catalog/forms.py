from django import forms
from django.core.exceptions import ValidationError
from .models import Product, Category

FORBIDDEN_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа',
    'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'purchase_price', 'is_published']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'category': forms.Select(),
        }

    #Валидация на запрещенные слова
    def clean_name(self):
        """Проверяем название на отсутствие запрещенных слов."""
        name = self.cleaned_data['name'].lower()
        for word in FORBIDDEN_WORDS:
            if word in name:
                raise ValidationError(f'Название содержит запрещенное слово: "{word}".')
        return name

    def clean_description(self):
        """Проверяем описание на отсутствие запрещенных слов."""
        description = self.cleaned_data.get('description', '').lower()
        for word in FORBIDDEN_WORDS:
            if word in description:
                raise ValidationError(f'Описание содержит запрещенное слово: "{word}".')
        return description

    #Валидация цены
    def clean_purchase_price(self):
        """Проверяем, что цена не отрицательная."""
        price = self.cleaned_data['purchase_price']
        if price < 0:
            raise ValidationError('Цена не может быть отрицательной.')
        return price

    #Стилизация форм
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем Bootstrap классы ко всем полям
        for field_name, field in self.fields.items():
            if field_name != 'is_published':
                # Для чекбокса будет отдельный класс
                field.widget.attrs['class'] = 'form-control'
            else:
                # Для булевого поля (чекбокса) - отдельная стилизация
                field.widget.attrs['class'] = 'form-check-input'