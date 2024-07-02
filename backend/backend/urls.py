from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from backend import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('companies/',       include('companies.urls',       namespace='company')),
    path('catalogs/',        include('catalogs.urls',        namespace='catalog')),
    path('builds/',          include('builds.urls',          namespace='build')),
    path('citizens/',        include('citizens.urls',        namespace='citizen')),
    path('achievements/',    include('achievements.urls',    namespace='achievement')),
    path('',                 include('main.urls',            namespace='main')),
    
    # path("__debug__/",       include("debug_toolbar.urls")),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)