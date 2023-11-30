



from . import views
from django.urls import path,include
from rest_framework import routers
# router1 = routers.DefaultRouter()

# router1.register(r'register', views.RegisterAPIView, basename='User')



urlpatterns = [
        path('sch',views.createNutritionistScheduleAPIView.as_view(),name='sch'), #this is used
        path("createNutritionistSchedule",views.putNutritionistScheduleAPIView.as_view(),name='createNutritionistSchedule'),
        path('reserveAppointment/<int:id>/',views.UserReservationAppointmentsAPIView.as_view(),name='reserveAppointment'),#ReservationAppointmentsAPIView
        path('getNutrtionistappointments/<int:id>/',views.getNutritionistAppointmentsScheduleAPIView.as_view(),name='getNutrtionistappointments'),
        path('addQuestion',views.addQuestionAPIView.as_view(),name='addQuestion'),
        path('addAnswer',views.addAnswerAPIView.as_view(),name='addAnswer'),
        path("NutritionistReservation",views.getNutritionistReservationAppointmentsAPIView.as_view(),name="NutritionistReservation"),
        path("userappointment",views.getUserReservationAppointmentsAPIView.as_view(),name="userAppointment"),
         path("userappointmentChat",views.getUserReservationChatsAPIView.as_view(),name="userAppointmentChat"),
        path("nutritionestChat",views.getNutritionistChatAppointmentsAPIView.as_view(),name="NutritionestChat"),
path('getUserNCPdatacNU/<int:user_id>/',views.getUserInfoChatAPIView.as_view(),name="getUserNCPdatacNU"),
path('getUserNCPInfo',views.getUserNCPInfoAPIView.as_view(),name='getUserNCPInfo'),
]