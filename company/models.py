from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название компании')
    description = models.TextField(verbose_name='Описание')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    website = models.URLField(blank=True, null=True, verbose_name='Сайт')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Телефон')

    def __str__(self):
        return self.name
