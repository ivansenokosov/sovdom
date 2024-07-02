from django.db import models
from django.db.models import Q

class Regions_Types(models.Model):
    name = models.CharField(
        max_length=150,
        null=False,
        blank=False,
        unique=True,
        verbose_name="Наименование",
    )

    class Meta:
        db_table = "s_region_type"
        verbose_name = "Тип региона"
        verbose_name_plural = "Типы регионов"

    def __str__(self):
        return f"{self.name}"



class Regions(models.Model):
    name = models.CharField(
        max_length=150, null=False, blank=False, unique=True, verbose_name="Регион"
    )
    type = models.ForeignKey(
        to=Regions_Types, verbose_name="Тип", on_delete=models.CASCADE, default=None
    )

    class Meta:
        db_table = "s_region"
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"

    def __str__(self):
        return f"{self.name}"



class Cities(models.Model):
    region = models.ForeignKey(
        to=Regions, verbose_name="Региион", on_delete=models.CASCADE, default=None
    )
    name = models.CharField(
        max_length=150, null=False, blank=False, unique=False, verbose_name="Город"
    )
    ymap = models.CharField(
        max_length=50, unique=False, null=True, blank=True, verbose_name="Координаты"
    )

    class Meta:
        db_table = "s_city"
        verbose_name = "Город"
        verbose_name_plural = "Города"

    def __str__(self):
        return f"{self.name}"
    
    def count_builds(self):
        from builds.models import Builds
        number = Builds.objects.filter(street__city = self.id).exclude(Q(ymap__isnull=True) | Q(ymap__exact='')).count()
        return number


class Streets_Types(models.Model):
    name = models.CharField(
        max_length=150,
        null=False,
        blank=False,
        unique=False,
        verbose_name="Наименование",
    )

    class Meta:
        db_table = "s_street_type"
        verbose_name = "Тип улицы"
        verbose_name_plural = "Типы улиц"

    def __str__(self):
        return f"{self.name}"



class Streets(models.Model):
    city = models.ForeignKey(
        to=Cities, verbose_name="Город", on_delete=models.CASCADE, default=None
    )
    type = models.ForeignKey(
        to=Streets_Types, verbose_name="Тип", on_delete=models.CASCADE, default=None
    )
    name = models.CharField(
        max_length=150, null=False, blank=False, unique=False, verbose_name="Улица"
    )

    class Meta:
        db_table = "s_street"
        verbose_name = "Улица"
        verbose_name_plural = "Улицы"

    def __str__(self):
        return f"{self.name}"



class Roof_Materials(models.Model):
    name = models.CharField(
        max_length=150,
        null=False,
        blank=False,
        unique=True,
        verbose_name="Материал крышии",
    )

    class Meta:
        db_table = "s_roof_material"
        verbose_name = "Материал крыши"
        verbose_name_plural = "Материалы крыш"

    def __str__(self):
        return f"{self.name}"



class Wall_Materials(models.Model):
    name = models.CharField(
        max_length=150,
        null=False,
        blank=False,
        unique=True,
        verbose_name="Материал стен",
    )

    class Meta:
        db_table = "s_wall_material"
        verbose_name = "Материал стен"
        verbose_name_plural = "Материалы стен"

    def __str__(self):
        return f"{self.name}"



class Rule_Types(models.Model):
    name = models.CharField(
        max_length=150,
        null=False,
        blank=False,
        unique=True,
        verbose_name="Наименование",
    )

    class Meta:
        db_table = "s_rule_type"
        verbose_name = "Тип управления"
        verbose_name_plural = "Типы управления"

    def __str__(self):
        return f"{self.name}"



class Priority_Types(models.Model):
    name = models.CharField(
        max_length=150,
        null=False,
        blank=False,
        unique=True,
        verbose_name="Наименование",
    )

    class Meta:
        db_table = "s_priority_type"
        verbose_name = "Тип приоритетность дома"
        verbose_name_plural = "Типы приоритетность дома"

    def __str__(self):
        return f"{self.name}"



class Gas_Types(models.Model):
    name = models.CharField(
        max_length=150,
        null=False,
        blank=False,
        unique=True,
        verbose_name="Наименование",
    )

    class Meta:
        db_table = "s_gas_type"
        verbose_name = "Тип системы газоснабжения"
        verbose_name_plural = "Типы системы газоснабжения"

    def __str__(self):
        return f"{self.name}"
    


class Banks(models.Model):
    name = models.CharField(max_length=1000, null=False, blank=False, unique=False, verbose_name="Название")
    bik  = models.CharField(max_length=50, null=True, blank=True, unique=False, verbose_name="БИК")
    cor_account = models.CharField(max_length=50, null=True, blank=True, unique=False, verbose_name="Кор.счёт")
    addr = models.CharField(max_length=1000, null=True, blank=True, unique=False, verbose_name="Адрес")

    class Meta:
        db_table = "s_banks"
        verbose_name = "Банк"
        verbose_name_plural = "Банки"

    def __str__(self):
        return f"{self.name}, {self.bik}"    