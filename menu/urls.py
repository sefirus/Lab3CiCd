from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from menu import views

app_name = 'menu'
urlpatterns = [
    path('', views.menu, name='menu'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
