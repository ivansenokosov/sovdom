from django.db import models
from catalogs.models import Banks, Cities

class Companies(models.Model):
    full_name	= models.CharField(max_length=1000, null=False, blank=False, unique=False, verbose_name="Полное наименование")
    short_name	= models.CharField(max_length=255, null=False, blank=False, unique=False, verbose_name="Краткое наименование")
    ogrn        = models.CharField(max_length=50, null=True, blank=True, unique=False, verbose_name="ОГРН")
    inn	        = models.CharField(max_length=50, null=True, blank=True, unique=False, verbose_name="ИНН")
    kpp	        = models.CharField(max_length=50, null=True, blank=True, unique=False, verbose_name="КПП")
    web_site	= models.CharField(max_length=255, null=True, blank=True, unique=False, verbose_name="Сайт")
    email	    = models.EmailField(max_length=255, null=True, blank=True, unique=False, verbose_name="email")
    bank        = models.ForeignKey(to = Banks, blank=True, null=True, on_delete = models.CASCADE, verbose_name="Банк", default = 1)
    account	    = models.CharField(max_length=50, null=True, blank=True, unique=False, verbose_name="Счёт")
    addr_jur	= models.CharField(max_length=1000, null=True, blank=True, unique=False, verbose_name="Адрес юридический")
    addr_post	= models.CharField(max_length=1000, null=True, blank=True, unique=False, verbose_name="Адрес почтовый")
    city        = models.ForeignKey(to = Cities, blank=False, null=False, on_delete = models.CASCADE, verbose_name="Город", default = 1)

    class Meta:
        db_table = "d_companies"
        verbose_name = "Оргнанизация"
        verbose_name_plural = "Оргнанизации"

    def __str__(self):
        return f"{self.short_name}, {self.inn}"


