from django.contrib import admin
from .models import Product, FavoriteProducts
# Register your models here.
admin.site.register(Product)

admin.site.register(FavoriteProducts)