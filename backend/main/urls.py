from django.urls import path

from main import views

app_name = 'main'

urlpatterns = [
    path('json', views.get_json, name='json'),
    path('micro_details_json', views.get_micro_details_json_view, name='get_micro_details_json'),
    path('map_json', views.map_json, name='map_json'),
]