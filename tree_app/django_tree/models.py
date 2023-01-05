from django.db import models


class MenuItem(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя меню', default='main')
    label = models.CharField(max_length=255, verbose_name='Название')
    link = models.CharField(max_length=255, verbose_name='Ссылка')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True, verbose_name='Родитель')

    def __str__(self):
        return self.label
