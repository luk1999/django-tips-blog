from django.conf.urls import url

from client_app.views import PostListView


app_name = 'client_app'
urlpatterns = [
    url(r'^$',PostListView.as_view(), name='index'),
]
