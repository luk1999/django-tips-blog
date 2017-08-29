from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('client_app.urls', namespace='client')),
]
