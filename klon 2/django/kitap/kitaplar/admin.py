from django.contrib import admin

# Register your models here.
from .models import Kitap

@admin.register(Kitap)
class KitapAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_published_time', 'get_price']
    list_filter = ['published_time']
    search_fields = ['title', 'content']

    def get_published_time(self, obj):
        return obj.published_time if obj.published_time else '-'
    get_published_time.short_description = 'Yayın Tarihi'

    def get_price(self, obj):
        return f'{obj.price} TL' if obj.price else '-'
    get_price.short_description = 'Fiyat'