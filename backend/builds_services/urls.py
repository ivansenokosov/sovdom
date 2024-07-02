from django.urls import path
from builds_services import views

from django.urls import path
from builds_services import views
from rest_framework.routers import DefaultRouter

app_name = 'build_sevice'


router = DefaultRouter()
router.register('', views.BuildServiceContainerViewset, 'service_containers')
urlpatterns = router.urls