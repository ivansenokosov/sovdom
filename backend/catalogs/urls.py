app_name = 'catalogs'

from django.urls import path
from catalogs import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('cities', views.CitiesViewset, 'cities')
router.register('cities_ymap', views.CitiesYMAPViewset, 'cities_ymap')
router.register('builds', views.BuildsViewset, 'builds')






urlpatterns = router.urls
