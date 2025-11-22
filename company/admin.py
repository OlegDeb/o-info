from django.contrib import admin
from .models import *



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    verbose_name = 'Категория'
    verbose_name_plural = 'Категории'


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description')
    list_filter = ('category',)
    search_fields = ('name',)
    verbose_name = 'Подкатегория'
    verbose_name_plural = 'Подкатегории'


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'subcategory', 'address', 'phone')
    list_filter = ('subcategory', 'subcategory__category')
    search_fields = ('name', 'description')
    verbose_name = 'Компания'
    verbose_name_plural = 'Компании'

