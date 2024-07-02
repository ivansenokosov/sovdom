from django.db import models
from catalogs.models import *
from companies.models import Companies
from django.db.models import Sum
from backend.sql_select import sql_select

class Builds(models.Model):
    city = models.ForeignKey(
         to=Cities, verbose_name="Город", on_delete=models.CASCADE, default = 1
    )  
    street = models.ForeignKey(
        to=Streets, verbose_name="Улица", on_delete=models.CASCADE,  related_name="cities"
    )
    number = models.CharField(
        max_length=10, unique=False, null=True, blank=True, verbose_name="Номер"
    )
    litera = models.CharField(
        max_length=30, unique=False, null=True, blank=True, verbose_name="Литера"
    )
    corpse = models.CharField(
        max_length=30, unique=False, null=True, blank=True, verbose_name="Корпус"
    )
    ymap = models.CharField(
        max_length=50, unique=False, null=True, blank=True, verbose_name="Координаты"
    )

    priority = models.ForeignKey(
        to=Priority_Types,
        verbose_name="Приоритетность",
        on_delete=models.CASCADE,
        blank=True, 
        null=True,
        default = 1
    )

    photo = models.ImageField(
        upload_to="builds_images", blank=True, null=True, verbose_name="Изображение"
    )

    year = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="Год постройки"
    )
    floors = models.PositiveSmallIntegerField(
        null=True, blank=True, verbose_name="Этажей"
    )
    q_porchs = models.PositiveSmallIntegerField(
        null=True, blank=True, verbose_name="Подъездов"
    )
    q_lifts = models.PositiveSmallIntegerField(
        null=True, blank=True, verbose_name="Лифтов"
    )
    q_flats = models.PositiveSmallIntegerField(
        null=True, blank=True, verbose_name="Квартир"
    )

    q_uu = models.PositiveSmallIntegerField(
        null=True, blank=True, verbose_name="Узлов учёта тепловой энергии"
    )

    s_live = models.DecimalField(
        default=0.00,
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Площадь жилых помещений",
    )
    s_no_live = models.DecimalField(
        default=0.00,
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Площадь нежилых помещений",
    )
    s_mop = models.DecimalField(
        default=0.00,
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Площадь МОП",
    )

    s_zem = models.DecimalField(
        default=0.00,
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Площадь земельного участка",
    )
    kadnum_zem = models.CharField(
        max_length=50,
        unique=False,
        null=True,
        blank=True,
        verbose_name="Кадастровый номер",
    )

    gas_type = models.ForeignKey(
        to=Gas_Types, verbose_name="Тип системы газоснабжения", on_delete=models.CASCADE, blank=True, null=True, default = 3
    )
    wall_material = models.ForeignKey(
        to=Wall_Materials, verbose_name="Материал стен", on_delete=models.CASCADE, blank=True, null=True,
    )
    roof_material = models.ForeignKey(
        to=Roof_Materials, verbose_name="Материал крыши", on_delete=models.CASCADE, blank=True, null=True, default = 2, 
    )

    has_garret = models.BooleanField(default=False, verbose_name="Наличие чердака", blank=True, null=True,)

    class Meta:
        db_table = "d_build"
        verbose_name = "Дом"
        verbose_name_plural = "Дома"

    def addr(self):
        addr = f"{self.street.name}, {self.number}"
        if self.litera!=None:
            addr += f"{self.litera}"

        if self.corpse!=None:
            addr += f"/{self.corpse}"

        return addr

    def addr1(self):
        return f"{self.street.city.name}, {self.addr()}"

    def __str__(self):
        return self.addr1()


    def s(self):
        return float(self.s_live + self.s_no_live)
    
    def uu(self):
        return 1
    
    def citizens(self):
        from citizens.models import Citizens
        return Citizens.objects.filter(build_id = self.build_id).count()
    
    def management(self):
        company = BuildManagement.objects.filter(build = self.pk).order_by('date').first()
        if company:
            return company
        else:
            return None

    def management_name(self):
        company =  BuildManagement.objects.filter(build = self.pk).order_by('date').first()
        if company:
            return Companies.objects.get(pk = company.company_id).short_name
        else:
            return None

    def report_number(self):
        from builds_services.models import BuildServiceContainer
        number = BuildServiceContainer.objects.filter(build_id = self.id).filter(type = 3).count()
        return number
    
    def total_rub(self):
        from builds_services.models import BuildServiceContainer
        return float(BuildServiceContainer.objects.filter(build_id = self.id).filter(type = 3).aggregate(rub = Sum('total_rub')).get('rub') or 0)
    
    def report_rub(self):
        from builds_services.models import BuildsServices
        return float(BuildsServices.objects.filter(container__build_id = self.id).filter(container__type_id = 3).aggregate(sum = Sum('cost')).get('sum') or 0) * 12 * self.s()

    def management_rub(self):
        from builds_services.models import BuildsServices
        return float(BuildsServices.objects.filter(container__build_id = self.id).filter(container__type_id = 3).filter(subgroup__group = 760).aggregate(sum = Sum('cost')).get('sum') or 0) * 12 * self.s()

    def repair_rub(self):
        from builds_services.models import BuildsServices
        return float(BuildsServices.objects.filter(container__build_id = self.id).filter(container__type_id = 3).filter(is_repair = 1).aggregate(sum = Sum('cost')).get('sum') or 0) * 12 * self.s() 


class BuildManagement(models.Model):
    build = models.ForeignKey(to = Builds, verbose_name="Организация", on_delete=models.CASCADE)
    date = models.DateField(null = True, blank = True, auto_now = False, auto_now_add = False, verbose_name = 'Дата начала упарвления', default = '01.01.2009')
    company = models.ForeignKey(to = Companies, verbose_name="Организация", on_delete=models.CASCADE)

    class Meta:
        db_table = "z_build_management"
        verbose_name = "Управляющая компания"
        verbose_name_plural = "Управляющие компании"

    def __str__(self):
        return f"{self.build.addr} - {self.company.short_name}"
    

class BuildSummary(models.Model):
    build = models.ForeignKey(to = Builds, verbose_name="Дом", on_delete=models.CASCADE)
    city_str = models.CharField(max_length=3000, unique=False, null=True, blank=True, verbose_name="Город")
    addr_str = models.CharField(max_length=3000, unique=False, null=True, blank=True, verbose_name="Улица")
    management_company_name = models.CharField(max_length=3000, unique=False, null=True, blank=True, verbose_name="Управляющая компания")
    report_number = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Отчётов")
    uu_number = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Количество узлов учёта")

    class Meta:
        db_table = "z_build_summary"
        verbose_name = "Сводная таблица по домам"
        verbose_name_plural = "Сводная таблица по домам"

    def __str__(self):
        return f"{self.city_str} - {self.addr_str}"