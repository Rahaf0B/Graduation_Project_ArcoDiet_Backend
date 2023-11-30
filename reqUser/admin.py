from django.contrib import admin
from .models import User,Allergies,Diseases,reqUser,Nutritionist,FavoriteNutritionists#,AppointmentTime,AppointmentDate,AppointmentDateSchedule#,UserNutritionistRelation,Appointment,NutritionistSchedule

admin.site.register(User)
admin.site.register(Allergies)
admin.site.register(Diseases)
admin.site.register(reqUser)
admin.site.register(Nutritionist)
admin.site.register(FavoriteNutritionists)