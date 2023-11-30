from datetime import datetime, timedelta
from django.db import models
import datetime
from reqUser.models import User, Nutritionist, reqUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import datetime
import datetime


class ReservationAppointments(models.Model):
    reservation_id = models.AutoField(primary_key=True)
    appointmentReservationDate = models.DateField(
        _("appointmentReservationDates"),)
    appointmentReservationTime = models.TimeField(
        _("appointmentReservationTimes"),)
    appointmentReservationFinished = models.BooleanField(
        _("appointmentReservationFinished"), default=False,)
    appointmentNutritionistReservation = models.ForeignKey(
        Nutritionist, on_delete=models.CASCADE, related_name="NutritionistAppointmentsScheduleReservation")


class AppointmentSchedule(models.Model):
    nutritionist = models.ForeignKey(
        Nutritionist, on_delete=models.CASCADE, related_name="ScheduleNutritionist")
    appointmentDayDate = models.DateField(_("appointmentDayDate"))
    appointmentStart_time = models.TimeField(_("appointmentStart_time"))
    appointmentEnd_time = models.TimeField(_("appointmentEnd_time"))
    available = models.BooleanField(_("availableAppointment"), default=True)

    appointmentReservationFinished = models.BooleanField(
        _("appointmentTimeFinished"), default=False,)

    class Meta:
        unique_together = (
            'nutritionist', 'appointmentDayDate', 'appointmentStart_time')

    def __str__(self):
        return f'{self.nutritionist} - {self.appointmentDayDate} - {self.appointmentStart_time}'

    def save(self, *args, **kwargs):
        if not isinstance(self.appointmentDayDate, datetime.date):
            date_obj = datetime.datetime.strptime(
                self.appointmentDayDate, '%Y-%m-%d').date()
            time_obj = datetime.datetime.strptime(
                self.appointmentStart_time, '%H:%M:%S').time()
            start_datetime = datetime.datetime.combine(date_obj, time_obj)
            end_datetime = start_datetime + timedelta(hours=1)
            self.appointmentEnd_time = end_datetime.time().strftime('%H:%M:%S')
        super().save(*args, **kwargs)

    @property
    def is_valid(self):
        start_datetime = datetime.combine(
            self.appointmentDayDate, self.appointmentStart_time)
        end_datetime = datetime.combine(
            self.appointmentDayDate, self.appointmentEnd_time)
        return start_datetime < end_datetime and self.appointmentDayDate >= datetime.today().date()


class userReservationAppointment(models.Model):
    Reservationuserid = models.AutoField(primary_key=True)
    appointmentReservation = models.ManyToManyField(
        AppointmentSchedule, related_name="appointmentReservation")

    Reservationuser = models.OneToOneField(
        reqUser, on_delete=models.CASCADE, related_name="ReservationUser")


class NCPForm(models.Model):
    Question = models.CharField(
        _("Question"), max_length=120, blank=True, null=True)

    def __str__(self):

        return str(self.Question)


class UserNCPForm(models.Model):
    NCPFormQuestion = models.ForeignKey(
        NCPForm, on_delete=models.CASCADE, related_name="NCPFormData")
    AnswerDescription = models.TextField(
        _("AnswerDescription"), blank=True, null=True)
    user = models.ForeignKey(
        reqUser, on_delete=models.CASCADE, related_name="reqUserNCP")
    QuestionAnswer = models.BooleanField(_("QuestionAnswer"), default=False)
