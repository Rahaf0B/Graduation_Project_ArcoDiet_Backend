from . import views
from django.urls import path


urlpatterns = [
    path('registerReqUser',views.RegisterReqUserAPIView.as_view(),name="registerReqUser"),
    path('registerNutritionistUser',views.RegisterNutritionistUserAPIView.as_view(),name="registerNutritionistUser"),
    path('info/<int:user_id>/',views.AddInformationAPIView.as_view(),name='info'),
    path('login',views.LoginAPIView.as_view(),name="login"),
    path('user',views.AuthUserAPIView.as_view(),name="user"),
    path('nutritionist',views.AuthNutritionistAPIView.as_view(),name='nutritionist'),   
    path('userId',views.GetUserIDAPIView.as_view(),name='userId'),
    path('allergies',views.AlergiesDiseasesAPIView.as_view(),name='allergies'),
    path('addallergy',views.AddAllergiesAPIView.as_view(),name='addallergy'),
    path('adddisease',views.AddDiseasesAPIView.as_view(),name='adddisease'),
    path('getallergies',views.getAllergiesAPIView.as_view(),name='getallergies'),
    path('getalldisease',views.getAllDiseasesAPIView.as_view(),name='getalldisease'),
  

]
