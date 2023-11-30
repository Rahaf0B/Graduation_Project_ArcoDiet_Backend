
from rest_framework import serializers
from .models import userReservationAppointment, AppointmentSchedule, UserNCPForm, NCPForm
from reqUser.models import reqUser, User, Nutritionist
from reqUser.serializers import getDiseasesSerializer, getAllergiesSerializer


class getNutritionistAppointmentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = AppointmentSchedule
        fields = ("nutritionist", "appointmentDayDate",
                  "appointmentStart_time", "appointmentEnd_time", "available")


class getNutritionistAppointmentsStartTimeEndTimeSerializers(serializers.ModelSerializer):
    class Meta:
        model = AppointmentSchedule
        fields = ("appointmentDayDate", "appointmentStart_time",
                  "appointmentEnd_time")


class addQuestionSerializers(serializers.ModelSerializer):
    class Meta:
        model = NCPForm
        fields = ("Question",)


class addAnswersSerializers(serializers.ModelSerializer):
    NCPFormQuestion = addQuestionSerializers(required=True)

    class Meta:
        model = UserNCPForm
        fields = ("user", "NCPFormQuestion",
                  "AnswerDescription", "QuestionAnswer")


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("user_id", "username", "profile_pic")


class reqUserInfoSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(required=True)

    class Meta:
        model = reqUser
        fields = ("user",)


class getNutritionistReservationAppointmentsSerializers(serializers.ModelSerializer):
    Reservationuser = reqUserInfoSerializer(required=True)
    appointmentReservation = getNutritionistAppointmentsSerializers(
        required=True, many=True)

    class Meta:
        model = userReservationAppointment
        fields = ("Reservationuser", "appointmentReservation")


class getUserReservationAppointmentsSerializers(serializers.ModelSerializer):

    class Meta:
        model = userReservationAppointment
        fields = ("Reservationuser", "appointmentReservation")


class getUserInfoChatSerializer(serializers.ModelSerializer):

    allergies = getAllergiesSerializer(required=True, many=True)
    diseases = getDiseasesSerializer(required=True, many=True)

    class Meta:
        model = User
        fields = ("username", "gender", "date_of_birth",
                  "allergies", "diseases", "weight", "height")


class reqUserncpInfoSerializer(serializers.ModelSerializer):
    user = getUserInfoChatSerializer(required=True)

    class Meta:
        model = reqUser
        fields = ("user",)


class getNCPAnswerserializer(serializers.ModelSerializer):
    NCPFormQuestion = addQuestionSerializers(required=True)

    class Meta:
        model = UserNCPForm
        fields = ("NCPFormQuestion", "AnswerDescription", "QuestionAnswer")
