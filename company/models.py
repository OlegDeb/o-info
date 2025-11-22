from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(unique=True, blank=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Subcategory(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название подкатегории')
    slug = models.SlugField(unique=True, blank=True, verbose_name='URL')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories', verbose_name='Категория')
    description = models.TextField(blank=True, null=True, verbose_name='Описание подкатегории')

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Subcategory.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('subcategory_detail', kwargs={'category_slug': self.category.slug, 'slug': self.slug})

    def __str__(self):
        return f"{self.category.name} - {self.name}"

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        # Уникальность slug в рамках категории
        unique_together = ['category', 'slug']


class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название компании')
    slug = models.SlugField(unique=True, blank=True, verbose_name='URL')
    description = models.TextField(verbose_name='Описание компании')
    address = models.CharField(max_length=255, verbose_name='Адрес компании')
    website = models.URLField(blank=True, null=True, verbose_name='Сайт компании')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Телефон компании')
    subcategory = models.ForeignKey('Subcategory', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Подкатегория')

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Company.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('company_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'