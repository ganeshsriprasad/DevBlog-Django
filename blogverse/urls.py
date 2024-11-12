from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
urlpatterns = [
    
    path('', include('home.urls')),
    path('dashboard/', include('admin_panel.urls')),
    path('eha/donttrytohackadminpagethis-is-the-universal-admin-panel-lol/', admin.site.urls ),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)