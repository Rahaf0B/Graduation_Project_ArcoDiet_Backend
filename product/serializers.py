

from rest_framework import serializers
from .models import Product, FavoriteProducts

class AddProductSerializer(serializers.ModelSerializer):

    class Meta:
        model=Product
        fields = '__all__'


        

class FavoriteProductSerializer(serializers.ModelSerializer):
    product=AddProductSerializer(required=True,many=True)

    class Meta:
        model = FavoriteProducts
        fields=('product',)