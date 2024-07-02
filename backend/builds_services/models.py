from django.db import models
from builds.models import Builds
from catalogs.models import Cities
from django.db.models import Q
from django.db.models import Sum


class BuildServiceContainerTypes(models.Model): # загружено
    name = models.CharField(max_length=1000, null=False, blank=False, unique=False, verbose_name="Наименование")

    class Meta:
        db_table = "s_builds_service_container_types"
        verbose_name = "Тип контейнера работ для дома"
        verbose_name_plural = "Типы контейнера работ для дома"

    def __str__(self):
        return f"{self.name}"


class BuildServiceContainerUnits(models.Model): # загружено
    name = models.CharField(max_length=1000, null=False, blank=False, unique=False, verbose_name="Наименование")

    class Meta:
        db_table = "s_builds_service_container_units"
        verbose_name = "Единица измерения для контейнера работ для дома"
        verbose_name_plural = "Единицы измерения для контейнера работ для дома"

    def __str__(self):
        return f"{self.name}"
 

class BuildServicePeriods(models.Model): # загружено
    name = models.CharField(max_length=1000, null=False, blank=False, unique=False, verbose_name="Наименование")
    name_v = models.CharField(max_length=1000, null=True, blank=True, unique=False, verbose_name="Наименование (винительный падеж)")

    class Meta:
        db_table = "s_builds_service_periods"
        verbose_name = "Периодичность"
        verbose_name_plural = "Периодичности"

    def __str__(self):
        return f"{self.name}"


class ServiceAnalyzeActions(models.Model): # загружено
    name = models.CharField(max_length=1000, null=False, blank=False, unique=False, verbose_name="Наименование")

    class Meta:
        db_table = "s_service_analyze_actions"
        verbose_name = "Действие при анализе"
        verbose_name_plural = "Действия при анализе"

    def __str__(self):
        return f"{self.name}"
    

class RepairAnalyzeActions(models.Model): # загружено
    name = models.CharField(max_length=1000, null=False, blank=False, unique=False, verbose_name="Наименование")

    class Meta:
        db_table = "s_repair_analyze_actions"
        verbose_name = "Действие при анализе ТР"
        verbose_name_plural = "Действия при анализе ТР"

    def __str__(self):
        return f"{self.name}"
        

class AnalyzeActionReasons(models.Model): # загружено
    name = models.CharField(max_length=1000, null=False, blank=False, unique=False, verbose_name="Наименование")

    class Meta:
        db_table = "s_analyze_action_reasons"
        verbose_name = "Осноание действия при анализе"
        verbose_name_plural = "Осноания действия при анализе"

    def __str__(self):
        return f"{self.name}"
    

class CostContainerDenominators(models.Model):  # загружено
    name = models.CharField(max_length=1000, null=False, blank=False, unique=False, verbose_name="Наименование")

    class Meta:
        db_table = "s_cost_container_denominators"
        verbose_name = "Знаменатель"
        verbose_name_plural = "Знаменатели"

    def __str__(self):
        return f"{self.name}"


class BuildServiceContainer(models.Model):
    type = models.ForeignKey(to = BuildServiceContainerTypes, blank=False, null=False, on_delete = models.CASCADE, verbose_name="Тип")
    city = models.ForeignKey(to = Cities, blank=True, null=True, on_delete = models.CASCADE, verbose_name="Город", default = None)
    build = models.ForeignKey(to = Builds, blank=True, null=True, on_delete = models.CASCADE, verbose_name="Дом", default = None)
    name = models.CharField(max_length=1000, null=False, blank=False, unique=False, verbose_name="Наименование")
    dbegin = models.DateField(null=False, blank=False, unique=False, verbose_name="Дата начала")
    dend = models.DateField(null=True, blank=True, unique=False, verbose_name="Дата окончания")
    total_rub = models.DecimalField(default=0.00, max_digits=15, decimal_places=2, null=True, blank=True, unique=False, verbose_name="Начислено за период")
    unit = models.ForeignKey(to = BuildServiceContainerUnits, blank=False, null=False, default = 1, on_delete = models.CASCADE, verbose_name="Единица измерения")

    class Meta:
        db_table = "d_build_service_container"
        verbose_name = "Контейнер работ для дома"
        verbose_name_plural = "Контейнеры работ для дома"

    def __str__(self):
        return f"{self.name}"


    def months(self):
        month_begin = int(self.dbegin.strftime('%m'))
        month_end = int(self.dend.strftime('%m'))
        return int(month_end - month_begin + 1)

    # количество работ в контейнере
    def count_services(self):
        from builds_services.models import BuildsServices
        count = BuildsServices.objects.filter(container_id = self.id).count()
        return count

    def get_services_sum(self, p_group_id, p_is_repair):
        from builds_services.models import BuildsServices


        query = Q()
        query &= Q(container_id = self.id)


        if p_group_id != -1:
            query &= Q(subgroup__group_id = p_group_id)

        if p_is_repair != -1:
            query &= Q(is_repair = p_is_repair)

        services = BuildsServices.objects.all().filter(query)
        sum = services.aggregate(services_cost = Sum('cost'))

        if sum.get('services_cost') != None:
            return float(sum.get('services_cost'))
        else:
            return 0

    # определение ставки платы по отчёту
    def get_stavka_container_by_report(self):

        # сначала ищем утверждённую ставку платы для этого отчёта

        containers = BuildServiceContainer.objects.filter(build_id = self.build_id).filter(type = 2).filter(dend__gt = self.dbegin).filter(dend__lt = self.dend)

        if containers:
            return containers.first()
        
        # если не нашли, ищём решение ОСС
        containers = BuildServiceContainer.objects.filter(city = self.city).filter(type = 1).filter(dend__gt = self.dbegin).filter(dend__lt = self.dend)

        if containers:
            return containers.first()
        else:
            return self


class ServiceGroups(models.Model): # загружено
    name = models.CharField(max_length=1000, null=False, blank=False, unique=False, verbose_name="Наименование")
    name_sokr = models.CharField(max_length=500, null=False, blank=False, unique=False, verbose_name="Наименование сокращённое")
    color = models.CharField(max_length=6, null=True, blank=True, unique=False, verbose_name="Цвет")
    color2 = models.CharField(max_length=6, null=True, blank=True, unique=False, verbose_name="Цвет")

    class Meta:
        db_table = "s_service_groups"
        verbose_name = "Группа работ"
        verbose_name_plural = "Группы работ"

    def __str__(self):
        return f"{self.name}"


class ServiceSubgroups(models.Model): # загружено
    name = models.CharField(max_length=1000, null=False, blank=False, unique=False, verbose_name="Наименование")
    name_sokr = models.CharField(max_length=500, null=False, blank=False, unique=False, verbose_name="Наименование сокращённое")
    group =  models.ForeignKey(to = ServiceGroups, blank=False, null=False, on_delete = models.CASCADE, verbose_name="Группа")

    class Meta:
        db_table = "s_service_subgroups"
        verbose_name = "Подгруппа работ"
        verbose_name_plural = "Подгруппы работ"

    def __str__(self):
        return f"{self.name}"


class BuildsServiceConditions(models.Model): # загружено
    name = models.CharField(max_length=1000, null=False, blank=False, unique=False, verbose_name="Наименование")

    class Meta:
        db_table = "s_service_conditions"
        verbose_name = "Условие выполнения работы"
        verbose_name_plural = "Условия выполнения работы"

    def __str__(self):
        return f"{self.name}"


class BuildsServices(models.Model):
    container = models.ForeignKey(to = BuildServiceContainer, blank=False, null=False, on_delete = models.CASCADE, verbose_name="Контейнер")
    subgroup = models.ForeignKey(to = ServiceSubgroups, blank=False, null=False, on_delete = models.CASCADE, verbose_name="Подгруппа")
    to_290 = models.PositiveIntegerField(null = True, blank = True, unique = False, verbose_name="Работа из минимального перечня")
    name = models.CharField(max_length=3000, null=False, blank=False, unique=False, verbose_name="Наименование")
    name_sokr = models.CharField(max_length=500, null=False, blank=False, unique=False, verbose_name="Наименование сокращённое")
    cost = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, null = True, blank = True, unique = False, verbose_name="Цена")
    is_repair = models.BooleanField(default = False, verbose_name="Текущий ремонт")
    condition = models.ForeignKey(to = BuildsServiceConditions, blank=False, null=False, on_delete = models.CASCADE, verbose_name="Условие")
    mbegin = models.PositiveSmallIntegerField(null = True, blank = True, unique = False, verbose_name="Месяц начала выполнения")
    mend = models.PositiveSmallIntegerField(null = True, blank = True, unique = False, verbose_name="Месяц окончания выполнения")
    period = models.DecimalField(default=0.00, max_digits=6, decimal_places=2, null = True, blank = True, unique = False, verbose_name="Раз в")
    period_y = models.ForeignKey(to = BuildServicePeriods, blank=False, null=False, on_delete = models.CASCADE, verbose_name="Период")

    class Meta:
        db_table = "s_build_services"
        verbose_name = "Работы дома"
        verbose_name_plural = "Работы для домов"

    def __str__(self):
        return f"{self.name}"

class CostContainer(models.Model): # загружено
    name = models.CharField(max_length=1000, null=False, blank=False, unique=False, verbose_name="Наименование")
    full_name = models.CharField(max_length=1000, null=False, blank=False, unique=False, verbose_name="Наименование")
    subtitle = models.CharField(max_length=1000, null=False, blank=False, unique=False, verbose_name="Наименование")
    color1 = models.CharField(max_length=6, null=False, blank=False, unique=False, verbose_name="Цвет")
    color2 = models.CharField(max_length=6, null=False, blank=False, unique=False, verbose_name="Цвет")
    show_repair = models.BooleanField(default = False, verbose_name="Отображать текущие ремонты")
    show_avg = models.BooleanField(default = False, verbose_name="Отображать среднее")
    show_minmax = models.BooleanField(default = False, verbose_name="Отображать минимум и максимум")
    parent = models.PositiveIntegerField(null = True, blank = True, unique = False, verbose_name="Вышестоящий контейнер", default = None)
    work_name = models.CharField(max_length=1000, null=False, blank=False, unique=False, verbose_name="Наименование работ")
    repair_name = models.CharField(max_length=1000, null=False, blank=False, unique=False, verbose_name="Наименование текущих ремонтов")
    denominator = models.ForeignKey(to = CostContainerDenominators, blank=False, null=False, on_delete = models.CASCADE, verbose_name="Знаменталель") 
    display_order = models.PositiveSmallIntegerField(null = True, blank = True, unique = False, verbose_name="Порядок отображения")


    class Meta:
        db_table = "d_cost_container"
        verbose_name = "Контейнер для сравнения цен"
        verbose_name_plural = "Контейнеры для сравнения цен"

    def __str__(self):
        return f"{self.name}"



class BuildsServicesAnalize(models.Model):
    service = models.ForeignKey(to = BuildsServices, blank=False, null=False, on_delete = models.CASCADE, verbose_name="Контейнер")
    action = models.ForeignKey(to = ServiceAnalyzeActions, blank=False, null=False, on_delete = models.CASCADE, verbose_name="Действие при анализе")
    repair_action = models.ForeignKey(to = RepairAnalyzeActions, blank=False, null=False, on_delete = models.CASCADE, verbose_name="Действие при анализе ТР")
    is_citizen = models.BooleanField(default = False, verbose_name="Преложение жителей")
    action_reason = models.ForeignKey(to = AnalyzeActionReasons, blank=False, null=False, on_delete = models.CASCADE, verbose_name="Действие при анализе ТР")
    cost2 = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, null = True, blank = True, unique = False, verbose_name="Цена")
    services_in_container = models.PositiveIntegerField(null = True, blank = True, unique = False, verbose_name="Работ в контейнере цен для сравнения")
    period_comment = models.CharField(max_length=1000, null=False, blank=False, unique=False, verbose_name="Периодичность комментарий")
    cost_container = models.ForeignKey(to = CostContainer, blank=False, null=False, on_delete = models.CASCADE, verbose_name="Контейнер") 
    
    class Meta:
        db_table = "d_build_service_analyze"
        verbose_name = "Анализ работы"
        verbose_name_plural = "Анализ работы"

    def __str__(self):
        return f"{self.service.name}"
    
class CostContainerWorks(models.Model):
    cost_container = models.ForeignKey(to = CostContainer, blank=False, null=False, on_delete = models.CASCADE, verbose_name="Контейнер") 
    service = models.ForeignKey(to = BuildsServices, blank=False, null=False, on_delete = models.CASCADE, verbose_name="Работа из минимального перечня") 

    class Meta:
        db_table = "s_cost_container_services"
        verbose_name = "Работы контернера"
        verbose_name_plural = "Работы контернеров"

    def __str__(self):
        return f"{self.cost_container.name}"    


class CostContainerGroups(models.Model):
    cost_container = models.ForeignKey(to = CostContainer, blank=False, null=False, on_delete = models.CASCADE, verbose_name="Контейнер") 
    subgroup = models.ForeignKey(to = ServiceSubgroups, blank=False, null=False, on_delete = models.CASCADE, verbose_name="Подгруппа работ") 

    class Meta:
        db_table = "s_cost_container_groups"
        verbose_name = "Группы работы контернера"
        verbose_name_plural = "Группы работ контернеров"

    def __str__(self):
        return f"{self.cost_container.name}"  
    

class CostContainerPrices(models.Model):
    cost_container = models.ForeignKey(to = CostContainer, blank=False, null=False, on_delete = models.CASCADE, verbose_name="Контейнер") 
    year = models.PositiveIntegerField(blank = False, null = False, unique=False, verbose_name="Год")
    city = models.ForeignKey(to = Cities, blank=False, null=False, on_delete = models.CASCADE, verbose_name="Город") 
    price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, null = True, blank = True, unique = False, verbose_name="Цена")

    class Meta:
        db_table = "s_cost_container_prices"
        verbose_name = "Цена на работу для контернера"
        verbose_name_plural = "Цены на работы для контернеров"

    def __str__(self):
        return f"{self.cost_container.name}"  
    

class BuildCostContainers(models.Model):
    build = models.ForeignKey(to = Builds, blank=False, null=False, on_delete = models.CASCADE, verbose_name="Контейнер")
    cost_container = models.ForeignKey(to = CostContainer, blank=False, null=False, on_delete = models.CASCADE, verbose_name="Контейнер")

    class Meta:
        db_table = "z_build_cost_container"
        verbose_name = "Контейнер сравнеия цен для дома"
        verbose_name_plural = "Контейнеры сравнеия цен для домов"

    def __str__(self):
        return f"{self.build.addr1} - {self.cost_container.name}"      
    
class BuildCostContainerData(models.Model):
    build = models.ForeignKey(to = Builds, blank=False, null=False, on_delete = models.CASCADE, verbose_name="Контейнер")
    cost_container = models.ForeignKey(to = CostContainer, blank=False, null=False, on_delete = models.CASCADE, verbose_name="Контейнер дома")
    cost_rub = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, null = True, blank = True, unique = False, verbose_name="Стоимость")
    cost_tr_rub = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, null = True, blank = True, unique = False, verbose_name="Стоимость ТР")
    stavka_rub = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, null = True, blank = True, unique = False, verbose_name="Ставка платы") 
    stavka_tr_rub = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, null = True, blank = True, unique = False, verbose_name="Ставка ТР")
    year = models.PositiveIntegerField(blank = False, null = False, unique=False, verbose_name="Год")
    calc_date = models.DateField(null=False, blank=False, unique=False, verbose_name="Дата расчёта")

    class Meta:
        db_table = "z_build_cost_container_data"
        verbose_name = "Рассчитанные данные для контейнера сравнеия цен для дома"

    def __str__(self):
        return f"{self.build.addr1} - {self.cost_container.name}"      
    

class ContainerLoadDataRules(models.Model):
    name = models.CharField(max_length=1000, null=False, blank=False, unique=False, verbose_name="Наименование")
    type = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, null = True, blank = True, unique = False, verbose_name="Тип") # 1 - добавление, 2 - распределение
    is_repair = models.BooleanField(default = False, verbose_name="Текущий ремонт")

    class Meta:
        db_table = "s_report_load_rules"
        verbose_name = "Правила загрузки данных в отчёты"

    def __str__(self):
        return f"{self.name}" 


class ContainerLoadData(models.Model):
    container =  models.ForeignKey(to = BuildServiceContainer(), blank=False, null=False, on_delete = models.CASCADE, verbose_name="Контейнер дома")
    name = models.CharField(max_length=3000, null=False, blank=False, unique=False, verbose_name="Наименование")
    cost = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, null = True, blank = True, unique = False, verbose_name="Стоимость")
    is_repair = models.BooleanField(default = False, verbose_name="Текущий ремонт")
    rule = models.ForeignKey(to = ContainerLoadDataRules, blank=False, null=False, on_delete = models.CASCADE, verbose_name="Правило")
    to_290 = models.PositiveIntegerField(null = True, blank = True, unique = False, verbose_name = 'Работа из минимального перечня')
    subgroup_to_load = models.CharField(max_length=3000, null = True, blank = True, unique = False, verbose_name = 'Подгруппа работ')
    is_to_290 = models.BooleanField(default = False, verbose_name="Работа из минимального перечня")
    is_repair_sovdom = models.BooleanField(default = False, verbose_name="Текущий ремонт подтверждён")
    period = models.DecimalField(max_digits=5, decimal_places=2, null = True, blank = True, unique = False, verbose_name = 'период')
    period_y = models.CharField(max_length=100, null = True, blank = True, unique = False, verbose_name = 'период')
    period_additional = models.CharField(max_length=100, null = True, blank = True, unique = False, verbose_name = 'период')
    period_comment = models.CharField(max_length=100, null = True, blank = True, unique = False, verbose_name = 'период')

    class Meta:
        db_table = "d_container_raw_data"
        verbose_name = "Сырые данные для загрузки"

    def __str__(self):
        return f"{self.container.name} - {self.name}" 

