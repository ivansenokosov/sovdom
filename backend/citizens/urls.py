# from django.urls import path

# from citizens import views

# app_name = 'citizens'

# urlpatterns = [
# #    path('', views.index, name='index'),
# #    path('about/', views.about, name='about'),
#     path('enterdocs/', views.CitizenEnterdocsView.as_view(), name='enter_docs'),
#     path('printenterdocs/', views.CitizenPrintEnterdocs, name='printenterdocs'),
#     path('', views.Index.as_view(), name='index'),
#     path('filter/', views.CitizenFilterView.as_view(), name='filter_citizen'),
#     path('create/', views.CitizenCreateView.as_view(), name='create_citizen'),
#     path('update/<int:pk>', views.CitizenUpdateView.as_view(), name='update_citizen'),
#     path('read/<int:pk>', views.CitizenReadView.as_view(), name='read_citizen'),
#     path('delete/<int:pk>', views.CitizenDeleteView.as_view(), name='delete_citizen'),
#     path('citizens/', views.citizens, name='citizens'),
#     path('test_pdf/', views.test_pdf, name='test_pdf'),

# ]

from django.urls import path
from citizens import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('citizens', views.CitizenViewset, 'citizens')
urlpatterns = router.urls

app_name = 'citizens'
