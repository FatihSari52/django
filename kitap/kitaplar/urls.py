from django.urls import path
from . import views

urlpatterns = [
    path('', views.kitap_listesi, name='kitap_listesi'),
    path('kitap/<int:pk>/', views.kitap_detay, name='kitap_detay'),
    path('kitap/ekle/', views.kitap_ekle, name='kitap_ekle'),
    path('kitap/<int:pk>/duzenle/', views.kitap_duzenle, name='kitap_duzenle'),
    path('kitap/<int:pk>/sil/', views.kitap_sil, name='kitap_sil'),
] 