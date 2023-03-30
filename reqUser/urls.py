from . import views
from django.urls import path


urlpatterns = [
    path('register',views.RegisterAPIView.as_view(),name="register"),
    path('info/<int:user_id>/',views.AddInformationAPIView.as_view(),name='info'),
    path('login',views.LoginAPIView.as_view(),name="login"),
    path('user',views.AuthUserAPIView.as_view(),name="user"),
    path('userId',views.GetUserIDAPIView.as_view(),name='userId'),
    path('addallergy',views.AddAllergiesAPIView.as_view(),name='addallergy'),
    path('adddisease',views.AddDiseasesAPIView.as_view(),name='adddisease'),
    path('getallergies',views.getAllergiesAPIView.as_view(),name='getallergies'),
    path('getalldisease',views.getAllDiseasesAPIView.as_view(),name='getalldisease'),
  

]
