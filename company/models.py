from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from city.models import *



class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название категории')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    slug = models.SlugField(max_length=250, unique=True, verbose_name='Url')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Subcategory(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название подкатегории')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories', verbose_name='Категория')
    description = models.TextField(blank=True, null=True, verbose_name='Описание подкатегории')
    slug = models.SlugField(max_length=250, verbose_name='Url')

    def __str__(self):
        return f"{self.category.name} - {self.name}"

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        # Уникальность slug в рамках категории
        unique_together = [['category', 'slug']]


class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название компании')
    author = models.ForeignKey(User, related_name="company", on_delete=models.CASCADE, default=1)
    type_work = models.CharField("Вид деятельности", max_length=350, blank=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='companies', verbose_name='Подкатегория')
    city = models.ForeignKey(City, verbose_name="Город", on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=255, verbose_name='Адрес компании')
    website = models.URLField(blank=True, null=True, verbose_name='Сайт компании')
    phone = models.JSONField(default=list, blank=True, null=True, verbose_name='Телефон компании', help_text='Список телефонов в формате ["+7(499) 123-45-67"]')
    email = models.CharField("E-mail", max_length=250, blank=True, default='')
    social_link = models.JSONField(default=list, blank=True, null=True, verbose_name='Социальные сети', help_text='Список ссылок на социальные сети')
    work_time = models.CharField("Режим работы", max_length=250, blank=True)
    map_url = models.CharField("Ссылка на карту", max_length=250, blank=True)
    map_zn = models.CharField("Координаты", max_length=50, blank=True)
    description = models.TextField(verbose_name='Описание компании')
    uslugi = models.JSONField(default=list, blank=True, null=True, verbose_name='Услуги', help_text='Список услуг')
    status = models.IntegerField(default=0)
    public = models.BooleanField(verbose_name='Публиковать на сайте', default=True)
    logo = models.ImageField("Логотип", upload_to="logo/%Y/%m/%d/", blank=True)
    date_start = models.DateTimeField(default=timezone.now)
    date_update = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique=True, blank=True, verbose_name='Url')

    def __str__(self):
        return self.name
    
    def get_phones_display(self):
        """Возвращает список телефонов для удобного отображения"""
        if self.phone and isinstance(self.phone, list):
            return self.phone
        elif self.phone:
            # Если телефон хранится как строка (старый формат), возвращаем как список
            return [str(self.phone)]
        return []
    
    def get_social_links_display(self):
        """Возвращает список социальных сетей для удобного отображения"""
        if self.social_link and isinstance(self.social_link, list):
            return self.social_link
        elif self.social_link:
            # Если социальные сети хранятся как строка (старый формат), возвращаем как список
            return [str(self.social_link)]
        return []
    
    def get_uslugi_display(self):
        """Возвращает список услуг для удобного отображения"""
        if self.uslugi and isinstance(self.uslugi, list):
            return self.uslugi
        elif self.uslugi:
            # Если услуги хранятся как строка (старый формат), возвращаем как список
            return [str(self.uslugi)]
        return []

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'


class ProcessedFile(models.Model):
    """Таблица для записи информации об обработанных файлах"""
    file_name = models.CharField(max_length=255, unique=True, verbose_name='Название файла', 
                                 help_text='Название без нижнего подчеркивания, цифр и расширения')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='processed_files', 
                                    verbose_name='Подкатегория')
    date_processed = models.DateTimeField(default=timezone.now, verbose_name='Дата обработки')
    
    def __str__(self):
        return f"{self.file_name} - {self.subcategory.name}"
    
    class Meta:
        verbose_name = 'Обработанный файл'
        verbose_name_plural = 'Обработанные файлы'
        ordering = ['-date_processed']