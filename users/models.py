from django.db import models
import os
from django.core.files.storage import default_storage
from PIL import Image
# Create your models here.
from django.contrib.auth.models import User

CHOICES = (('male', "Мужской пол"), ('female', "Женский пол"))

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    img = models.ImageField('Фото пользователя', default='default.png', upload_to='user_images')
    sex = models.CharField(choices=CHOICES, default='male', verbose_name='Пол')
    agreed = models.BooleanField(default=True, verbose_name="Соглашение про отправку уведомлений на почту")

    def __str__(self):
        return f'Профайл пользователя {self.user.username}'

    def save(self, *args, **kwargs):
        # Получаем старый объект только если он существует в БД
        if self.pk:
            try:
                old = Profile.objects.get(pk=self.pk)
                # Обрабатываем удаление старого изображения
                if old.img and old.img != self.img:
                    if old.img.name != 'default.png' and default_storage.exists(old.img.path):
                        default_storage.delete(old.img.path)
            except Profile.DoesNotExist:
                old = None
        else:
            old = None  # Новый объект — старого состояния нет

        # Сохраняем объект в БД
        super().save(*args, **kwargs)

        # Обрабатываем изображение только если оно есть
        if self.img:
            try:
                image_path = self.img.path
                if default_storage.exists(image_path):
                    with Image.open(image_path) as image:
                        # Если изображение слишком большое — уменьшаем
                        if image.height > 256 or image.width > 256:
                            resize = (256, 256)
                            image.thumbnail(resize)
                            # Сохраняем изменённое изображение
                            image.save(image_path, quality=95, optimize=True)
            except (OSError, IOError) as e:
                print(f"Ошибка обработки изображения: {e}")

    class Meta:
        verbose_name = "Профайл"
        verbose_name_plural = "Профайлы"
