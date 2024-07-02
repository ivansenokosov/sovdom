from django.urls import path
from companies import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('company', views.CompanyViewset, 'company')
urlpatterns = router.urls

app_name = 'companies'

# urlpatterns = [
#     path(r'^$', views.CompanyListView.as_view(), name='index'),
#     path('create/', views.CompanyCreateView.as_view(), name='create'),
#     path('update/<int:pk>', views.CompanyUpdateView.as_view(), name='update'),
#     path('delete/<int:pk>', views.CompanyDeleteView.as_view(), name='delete'),
# ] 
