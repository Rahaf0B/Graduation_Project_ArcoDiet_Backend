from django.contrib import admin
from .models import AppointmentTime,AppointmentDate,AppointmentDateSchedule,ReservationAppointments,userReservationAppointment,AppointmentSchedule,NCPForm,UserNCPForm



admin.site.register(AppointmentTime)
admin.site.register(AppointmentDate)
admin.site.register(AppointmentDateSchedule)
admin.site.register(ReservationAppointments)

admin.site.register(userReservationAppointment)
admin.site.register(AppointmentSchedule)
admin.site.register(NCPForm)
admin.site.register(UserNCPForm) 
