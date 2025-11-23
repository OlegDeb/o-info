from django.db import models



class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(max_length=250, unique=True, verbose_name='Url')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Subcategory(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название подкатегории')
    slug = models.SlugField(max_length=250, verbose_name='Url')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories', verbose_name='Категория')
    description = models.TextField(blank=True, null=True, verbose_name='Описание подкатегории')

    def __str__(self):
        return f"{self.category.name} - {self.name}"

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        # Уникальность slug в рамках категории
        unique_together = [['category', 'slug']]


class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название компании')
    slug = models.SlugField(max_length=250, unique=True, verbose_name='Url')
    description = models.TextField(verbose_name='Описание компании')
    address = models.CharField(max_length=255, verbose_name='Адрес компании')
    website = models.URLField(blank=True, null=True, verbose_name='Сайт компании')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Телефон компании')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='companies', verbose_name='Подкатегория')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'