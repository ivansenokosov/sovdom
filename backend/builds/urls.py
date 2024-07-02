app_name = 'builds'

from django.urls import path
from builds import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', views.BuildsViewset, 'builds')
urlpatterns = router.urls

