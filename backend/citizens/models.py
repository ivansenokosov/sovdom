from django.db import models
from django.urls import reverse
from builds.models import Builds

class Citizens_type(models.Model):
    name = models.CharField(max_length=50, null = False, verbose_name='Тип')

    class Meta:
        db_table = 's_citizen_type'
        verbose_name = "Тип гражданина"
        verbose_name_plural = "Типы граждан"

    def __str__(self):
        return f'{self.name}'

class Citizens_status(models.Model):
    name = models.CharField(max_length=150, null = False, verbose_name='Статус')

    class Meta:
        db_table = 's_citizen_status'
        verbose_name = "Состояние гражданина"
        verbose_name_plural = "Состояния гражданина"

    def __str__(self):
        return f'{self.name}'


class Citizens(models.Model):
    family_name = models.CharField(max_length=150, null = False, blank=False, verbose_name='Фамилия')
    first_name = models.CharField(max_length=150, null = False, blank=False, verbose_name='Имя')
    second_name = models.CharField(max_length=150, null = False, blank=False, verbose_name='Отчество')

    family_name_r = models.CharField(max_length=150, null = True, blank = True, verbose_name='Фамилия в родительном падеже')
    first_name_r = models.CharField(max_length=150, null = True, blank = True, verbose_name='Имя в родительном падеже')
    second_name_r = models.CharField(max_length=150, null = True, blank = True, verbose_name='Отчество в родительном падеже')

    city_str = models.CharField(max_length=50, blank=True, null=True, verbose_name='Город')
    street_str = models.CharField(max_length=50, blank=True, null=True, verbose_name='Улица')
    build_str = models.CharField(max_length=30, blank=True, null=True, verbose_name='Дом')
    flat = models.CharField(max_length=10, blank=True, null=True, verbose_name='Квартира')

    comment = models.TextField(max_length=4000, blank=True, null=True, verbose_name='Комментарий')

    build = models.ForeignKey(to = Builds, verbose_name='Дом', on_delete=models.CASCADE)
    type = models.ForeignKey(to = Citizens_type, verbose_name='Тип', on_delete=models.CASCADE, default = 1) # Собственник, социальный найм, прочее

    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Телефон')
    email = models.EmailField(max_length=70, blank=True, unique=False, verbose_name='Имейл')
    status = models.ForeignKey(to = Citizens_status, verbose_name="Статус", on_delete=models.CASCADE, default = 1)
    
    date_create = models.DateField(auto_now_add=True, verbose_name='Дата создения', blank = True, null = True) # дата регистрации
    office_notification_date = models.DateField(verbose_name='Дата отправки уведомления в офис', blank = True, null = True)# дата уведомления офиса о регистрации
    uk_notification_date = models.DateTimeField(verbose_name='Дата отправки уведомления в управляющую компанию', blank = True, null = True) # дата уведомления управляющей компании о соглашении и заявлении в Совдом

    code = models.CharField(max_length=10, blank=True, null=True, verbose_name='Код из смс') # отправленный код
    code_date = models.DateTimeField(verbose_name='Дата отправки кода СМС', blank = True, null = True) # дата и время отравки кода

    class Meta:
        db_table = 'd_citizen'
        verbose_name = "Граждани"
        verbose_name_plural = "Граждане"

    def __str__(self):
        return f'{self.family_name} {self.first_name} {self.second_name}'

    def fio(self):
        return f'{self.family_name} {self.first_name} {self.second_name}'

    def fio_r(self):
        return f'{self.family_name_r} {self.first_name_r} {self.second_name_r}'

    def family_io(self):
        return f'{self.family_name} {self.first_name[0:1]}.{self.second_name[0:1]}.'

    def addr(self):
        return f'{self.build.addr1()}, кв. {self.flat}'
