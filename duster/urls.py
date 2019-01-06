from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'', include('main_app.urls')),
    url(r'', include('auth_app.urls')),
    ]
