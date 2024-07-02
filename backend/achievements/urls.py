from django.urls import path
from achievements import views
from rest_framework.routers import DefaultRouter

app_name = 'achievements'

router = DefaultRouter()
router.register('', views.AchievementsViewset, 'achievements')
urlpatterns = router.urls