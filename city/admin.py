from django.contrib import admin
from .models import FederalDistrict, Region, City


@admin.register(FederalDistrict)
class FederalDistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    verbose_name = 'Федеральный округ'
    verbose_name_plural = 'Федеральные округа'


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'federal_district', 'slug')
    list_filter = ('federal_district',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    verbose_name = 'Субъект РФ'
    verbose_name_plural = 'Субъекты РФ'


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'federal_district_display', 'slug')
    list_filter = ('region', 'region__federal_district')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    verbose_name = 'Город'
    verbose_name_plural = 'Города'

    def federal_district_display(self, obj):
        """Отображение федерального округа через регион"""
        return obj.region.federal_district.name if obj.region else '-'
    federal_district_display.short_description = 'Федеральный округ'
