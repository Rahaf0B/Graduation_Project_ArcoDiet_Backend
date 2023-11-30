from . import views
from django.urls import path,include
from rest_framework import routers


urlpatterns = [
    path('chatmsg/<int:receiver>/',views.getAllMSGAPIView.as_view(),name="chatmsg"),
    path('api/image-upload/', views.ImageUploadView.as_view(), name='image-upload'),

]