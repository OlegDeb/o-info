from django.db import models


class FederalDistrict(models.Model):
    name = models.CharField(max_length=250, unique=True, verbose_name="Название федерального округа")
    slug = models.SlugField(max_length=250, unique=True, verbose_name='Url')
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Федеральный округ"
        verbose_name_plural = "Федеральные округа"
        ordering = ['name']


class Region(models.Model):
    name = models.CharField(max_length=250, verbose_name="Название субъекта")
    federal_district = models.ForeignKey(FederalDistrict, on_delete=models.PROTECT, related_name='regions', verbose_name="Федеральный округ")
    slug = models.SlugField(max_length=250, verbose_name='Url')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Субъект РФ"
        verbose_name_plural = "Субъекты РФ"
        ordering = ['name']
        # Уникальность slug в рамках федерального округа
        unique_together = [['federal_district', 'slug']]


class City(models.Model):
    name = models.CharField(max_length=250, verbose_name="Название города")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='cities', verbose_name="Субъект РФ")
    slug = models.SlugField(max_length=250, verbose_name='Url')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"
        ordering = ['name']
        # Уникальность slug в рамках региона
        unique_together = [['region', 'slug']]