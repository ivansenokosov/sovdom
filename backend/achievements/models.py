from django.db import models
from builds.models import Builds


class Achievement(models.Model):
    db_table = "s_achievement"
    verbose_name = "Было/стало"
    verbose_name_plural = "Было/стало"    

    build        = models.ForeignKey(to = Builds, verbose_name='Дом', on_delete = models.CASCADE)
    name         = models.CharField(max_length=200, blank=True, verbose_name='Описание')
    year_before  = models.BigIntegerField(null = False, blank = True, verbose_name='Год до')
    photo_before = models.ImageField(upload_to="achieves_images", blank=True, null=True, verbose_name="Изображение до")
    info_before  = models.CharField(max_length=2000, blank=True, verbose_name='Описание до')

    year_after   = models.BigIntegerField(null = False, blank = True, verbose_name='Год после')
    photo_after  = models.ImageField(upload_to="achieves_images", blank=True, null=True, verbose_name="Изображение после")
    info_after   = models.CharField(max_length=2000, blank=True, verbose_name='Описание после')

    class Meta:
        db_table = "s_achievements"
        verbose_name = "Достижение"
        verbose_name_plural = "Достижения"

    def __str__(self):
        return f"{self.name}"