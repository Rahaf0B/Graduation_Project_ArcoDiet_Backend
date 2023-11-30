from . import views
from django.urls import path, include
from rest_framework import routers


urlpatterns = [
    path('addProduct', views.AddProductAPIView.as_view(), name="addProduct"),
    path('getProduct', views.getProductAPIView.as_view(), name="getProduct"),
    path('getAllProduct', views.getALLProductsAPIView.as_view(), name='getAllProduct'),
    path('addFavorite/<int:id>/',
         views.AddFavoriteProductsAPIView.as_view(), name='addFavorite'),
    path('deleteFavorite/<int:id>/',
         views.DeleteFavoriteProductAPIView.as_view(), name='deleteFavorite'),
    path('getFavorite', views.GetAllFavoriteProductAPIView.as_view(),
         name='getFavorite'),
    path('addEditProduct', views.PictureEmailAPIView.as_view(),
         name='addEditProduct'),
    path('helpAndSupport', views.HelpEmailAPIView.as_view(), name="helpAndSupport"),
    path('getproductbyid/<int:product_id>/',
         views.getProductByIDAPIView.as_view(), name='getproductbyid'),
]
