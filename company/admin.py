from django.contrib import admin
from .models import *



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    verbose_name = 'Категория'
    verbose_name_plural = 'Категории'


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug')
    list_filter = ('category',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    verbose_name = 'Подкатегория'
    verbose_name_plural = 'Подкатегории'


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'subcategory', 'address', 'phone', 'date_start', 'date_update')
    list_filter = ('subcategory', 'subcategory__category', 'date_start', 'date_update')
    search_fields = ('name', 'description')
    readonly_fields = ('date_start', 'date_update')
    verbose_name = 'Компания'
    verbose_name_plural = 'Компании'


@admin.register(ProcessedFile)
class ProcessedFileAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'subcategory', 'date_processed')
    list_filter = ('subcategory', 'date_processed')
    search_fields = ('file_name',)
    readonly_fields = ('date_processed',)
    verbose_name = 'Обработанный файл'
    verbose_name_plural = 'Обработанные файлы'

