from datetime import date, datetime, time
import json
from django.shortcuts import render
from .models import ReservationAppointments, userReservationAppointment, AppointmentSchedule, NCPForm, UserNCPForm
from reqUser.models import reqUser, Nutritionist, User
from rest_framework import response, status, permissions
from reqUser.jwt import JWTAuthentication
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializer import getNutritionistAppointmentsSerializers, addQuestionSerializers, addAnswersSerializers, getNutritionistReservationAppointmentsSerializers, getUserReservationAppointmentsSerializers, getUserInfoChatSerializer, reqUserncpInfoSerializer, getNCPAnswerserializer, reqUserInfoSerializer, getNutritionistAppointmentsStartTimeEndTimeSerializers
from operator import itemgetter
from itertools import groupby

from datetime import datetime


from django.db import transaction
from django.utils import timezone


class createNutritionistScheduleAPIView(GenericAPIView):
    permission_classes = ((permissions.IsAuthenticated,))
    authentication_classes = [JWTAuthentication]

    def put(self, request):
        nuUser = Nutritionist.objects.get(user=request.user)
        for timeofAppointment in request.data['appointmentTime']:
            timeAvailability = True
            try:

                timeAvailability = timeofAppointment["available"]
            except:
                timeAvailability = True

            try:
                appointmentdatatime = AppointmentSchedule.objects.get(appointmentStart_time=datetime.strptime(timeofAppointment["appointmentTime"], '%I:%M %p').time(
                ).strftime('%H:%M:%S'), available=timeAvailability, nutritionist=nuUser, appointmentDayDate=request.data["appointmentDate"])

            except:
                appointmentdatatime, appointmenttimecreated = AppointmentSchedule.objects.get_or_create(appointmentStart_time=datetime.strptime(
                    timeofAppointment["appointmentTime"], '%I:%M %p').time().strftime('%H:%M:%S'), available=timeAvailability, nutritionist=nuUser, appointmentDayDate=request.data["appointmentDate"])

        return response.Response({'message': 'The Schedule Appointment has been updated successfully'}, status=status.HTTP_200_OK)


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        if isinstance(obj, time):
            return obj.isoformat()
        return super().default(obj)


class getNutritionistAppointmentsScheduleAPIView(GenericAPIView):
    serializer_class = getNutritionistAppointmentsSerializers

    def post(self, request, id):
        user = User.objects.get(user_id=id)
        nutritionist = Nutritionist.objects.get(user=user)

        if (AppointmentSchedule.objects.filter(nutritionist=nutritionist, appointmentDayDate=request.data["appointmentDate"]).exists()):
            jsonData = json.dumps([appointment for appointment in AppointmentSchedule.objects.filter(
                nutritionist=nutritionist, appointmentDayDate=request.data["appointmentDate"]).values()], cls=DateEncoder)
            jsonData2 = json.loads(jsonData)
            datatoreturn = {"appointmentDayDate": "",
                            "appointmentStart_time": []}
            mergedData = {}
            index = 0
            for data in jsonData2:
                for key, value in data.items():
                    if key == "appointmentDayDate":
                        datatoreturn["appointmentDayDate"] = value
                    elif key == "appointmentStart_time":
                        datatoreturn["appointmentStart_time"].append(
                            {"appointmentStart_time": value, "available": True})
                    elif key == "available":
                        datatoreturn["appointmentStart_time"][index]["available"] = value
                        index = index+1

            json_output = json.dumps(mergedData)
            for data in datatoreturn["appointmentStart_time"]:
                data["appointmentStart_time"] = datetime.strptime(
                    data["appointmentStart_time"], '%H:%M:%S').time().strftime('%I:%M %p')
            return response.Response(datatoreturn, status=status.HTTP_201_CREATED)

        return response.Response({"error: this Nutritionist does not have any appointments"}, status=status.HTTP_400_BAD_REQUEST)


class UserReservationAppointmentsAPIView(GenericAPIView):
    permission_classes = ((permissions.IsAuthenticated,))
    authentication_classes = [JWTAuthentication]

    def put(self, request, id):

        appointmentTime = request.data['appointmentReservationTime']
        appointmentDate = request.data['appointmentReservationDate']
        user = request.user
        requser = reqUser.objects.get(user=user)
        nutritionestUser = User.objects.get(user_id=id)
        appointmentNutritionist = Nutritionist.objects.get(
            user=nutritionestUser)
        serializer = getNutritionistAppointmentsSerializers(AppointmentSchedule.objects.get(
            nutritionist=appointmentNutritionist, appointmentDayDate=appointmentDate, appointmentStart_time=datetime.strptime(appointmentTime, '%I:%M %p').time().strftime('%H:%M:%S')))

        with transaction.atomic():
            conflicting_appointments = ReservationAppointments.objects.filter(appointmentReservationTime=datetime.strptime(appointmentTime, '%I:%M %p').time(
            ).strftime('%H:%M:%S'), appointmentReservationDate=appointmentDate, appointmentNutritionistReservation=appointmentNutritionist)

            if conflicting_appointments.exists():
                transaction.set_rollback(True)
                return response.Response({'error': 'This time slot is already booked.'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                serializer = getNutritionistAppointmentsSerializers(AppointmentSchedule.objects.get(
                    nutritionist=appointmentNutritionist, appointmentDayDate=appointmentDate, appointmentStart_time=datetime.strptime(appointmentTime, '%I:%M %p').time().strftime('%H:%M:%S')))
            except:
                return response.Response({""}, status=status.HTTP_400_BAD_REQUEST)
            if ((serializer.data["appointmentStart_time"] == appointmentTime) & (serializer.data["available"] == True)):
                appointmentReservation = ReservationAppointments(appointmentReservationTime=datetime.strptime(appointmentTime, '%I:%M %p').time(
                ).strftime('%H:%M:%S'), appointmentReservationDate=appointmentDate, appointmentNutritionistReservation=appointmentNutritionist)
                appointmentReservation.save()
                appointment = AppointmentSchedule.objects.get(appointmentStart_time=datetime.strptime(appointmentTime, '%I:%M %p').time(
                ).strftime('%H:%M:%S'), appointmentDayDate=appointmentDate, nutritionist=appointmentNutritionist)
                ReservationUser = userReservationAppointment.objects.filter(
                    Reservationuser=requser)
                if not ReservationUser:
                    userReservation = userReservationAppointment(
                        Reservationuser=requser)
                    userReservation.save()
                else:
                    userReservation = userReservationAppointment.objects.get(
                        Reservationuser=requser)

                try:
                    appointmentTimeRes = userReservationAppointment.objects.filter(
                        Reservationuser=requser)
                    for appointments in appointmentTimeRes:
                        checkappointment = appointments.appointmentReservation.filter(
                            appointmentDayDate=appointmentDate, appointmentStart_time=datetime.strptime(appointmentTime, '%I:%M %p').time().strftime('%H:%M:%S'))
                        if checkappointment:
                            return response.Response({'error': 'You Already Have An Appointment on this Time'}, status=status.HTTP_409_CONFLICT)

                except:
                    ...
                userReservation.appointmentReservation.add(appointment)
                appointmenttimeobj = AppointmentSchedule.objects.get(appointmentDayDate=str(appointmentDate), appointmentStart_time=datetime.strptime(
                    appointmentTime, '%I:%M %p').time().strftime('%H:%M:%S'), nutritionist=appointmentNutritionist)
                appointmenttimeobj.available = False
                appointmenttimeobj.save()
                return response.Response({'success': 'Appointment Reservation created.'}, status=status.HTTP_201_CREATED)

            return response.Response({'error': 'The Appointment is not Available'}, status=status.HTTP_400_BAD_REQUEST)


class addQuestionAPIView(GenericAPIView):
    serializer_class = addQuestionSerializers

    def post(self, request):

        try:
            question = NCPForm.objects.get(Question=request.data["Question"])
            return response.Response({"error:This Question is already added"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class addAnswerAPIView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [JWTAuthentication]
    serializer_class = addAnswersSerializers

    def post(self, request):
        try:
            requser = reqUser.objects.get(user=request.user)

        except reqUser.DoesNotExist:
            return response.Response({"error": "reqUser does not exist."}, status=400)

        for AnswerData in request.data["Answers"]:
            try:
                question = NCPForm.objects.get(Question=AnswerData["Question"])
                try:
                    answerscreated = UserNCPForm.objects.get(
                        user=requser, NCPFormQuestion=question)
                    answerscreated.QuestionAnswer = AnswerData["QuestionAnswer"]
                    answerscreated.AnswerDescription = AnswerData["AnswerDescription"]
                    answerscreated.save()
                except:
                    answerscreated = UserNCPForm.objects.create(
                        user=requser, QuestionAnswer=AnswerData["QuestionAnswer"], AnswerDescription=AnswerData["AnswerDescription"], NCPFormQuestion=question)
            except NCPForm.DoesNotExist:
                return response.Response({"error": "NCPForm does not exist."}, status=400)
        return response.Response({"message": "Answers is already added"})


class getNutritionistReservationAppointmentsAPIView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        data = []
        nutritionist = Nutritionist.objects.get(user=request.user)
        try:
            appointment = AppointmentSchedule.objects.filter(
                nutritionist=nutritionist, appointmentDayDate=request.data['appointmentDate'], available=False)

            index = 0

            user_reservations = userReservationAppointment.objects.filter(
                appointmentReservation__nutritionist=nutritionist, appointmentReservation__appointmentDayDate=request.data['appointmentDate']).values("Reservationuser__user__username", "appointmentReservation")
            for userres in user_reservations:
                appointmentNU = AppointmentSchedule.objects.get(
                    id=userres['appointmentReservation'])
                serializer = getNutritionistAppointmentsStartTimeEndTimeSerializers(
                    appointmentNU)

                data.append(
                    {"user": userres['Reservationuser__user__username'], "appointment": serializer.data})

            grouped_data = {}
            for item in data:
                user = item['user']
                appointment = item['appointment']

                if user in grouped_data:
                    grouped_data[user].append(appointment)
                else:
                    grouped_data[user] = [appointment]

            result = [{"user": key, "appointments": value}
                      for key, value in grouped_data.items()]

            return response.Response(result, status=status.HTTP_200_OK)
        except:
            return response.Response({"message": "There is no appointment"}, status=status.HTTP_404_NOT_FOUND)


class getUserReservationAppointmentsAPIView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        user = reqUser.objects.get(user=request.user)
        appointment_date = request.data['appointmentDate']

        user_reservations = userReservationAppointment.objects.filter(
            Reservationuser=user, appointmentReservation__appointmentDayDate=appointment_date)
        appointments = AppointmentSchedule.objects.filter(
            id__in=user_reservations.values_list('appointmentReservation__id', flat=True))
        serialized_appointments = [{"id": appointment.id, "nutritionist": appointment.nutritionist.user.username, "appointmentStart_time": datetime.strptime(str(appointment.appointmentStart_time), '%H:%M:%S').time(
        ).strftime('%I:%M %p'), "appointmentEnd_time": datetime.strptime(str(appointment.appointmentEnd_time), '%H:%M:%S').time().strftime('%I:%M %p')} for appointment in appointments]

        sorted_appointments = sorted(
            serialized_appointments, key=itemgetter('nutritionist'))
        grouped_appointments = {key: list(group) for key, group in groupby(
            sorted_appointments, key=itemgetter('nutritionist'))}
        appointments_list = [{'nutritionist': key, 'appointments': value}
                             for key, value in grouped_appointments.items()]

        return response.Response(appointments_list)


class getUserReservationChatsAPIView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = reqUser.objects.get(user=request.user)
        user_reservations = userReservationAppointment.objects.filter(
            Reservationuser=user)
        appointments = AppointmentSchedule.objects.filter(
            id__in=user_reservations.values_list('appointmentReservation__id', flat=True))
        serialized_appointments = [{"id": appointment.nutritionist.user.user_id, "nutritionist": appointment.nutritionist.user.username, "profile_pic": "/media/"+(str(appointment.nutritionist.user.profile_pic)), "appointmentDayDate": appointment.appointmentDayDate, "appointmentStart_time": datetime.strptime(
            str(appointment.appointmentStart_time), '%H:%M:%S').time().strftime('%I:%M %p'), "appointmentEnd_time": datetime.strptime(str(appointment.appointmentEnd_time), '%H:%M:%S').time().strftime('%I:%M %p')} for appointment in appointments]
        sorted_appointments = sorted(
            serialized_appointments, key=itemgetter('nutritionist'))
        grouped_appointments = {key: list(group) for key, group in groupby(
            sorted_appointments, key=itemgetter('nutritionist'))}
        appointments_list = [{'nutritionist': key, 'appointments': value}
                             for key, value in grouped_appointments.items()]

        return response.Response(appointments_list)


class getNutritionistChatAppointmentsAPIView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        data = []
        nutritionist = Nutritionist.objects.get(user=request.user)
        try:
            appointment = AppointmentSchedule.objects.filter(
                nutritionist=nutritionist, available=False)
            for op in appointment:
                userReservation = userReservationAppointment.objects.get(
                    appointmentReservation=op)
                serializer = getNutritionistReservationAppointmentsSerializers(
                    userReservation)
                data.append(serializer.data)
            nu_names = set()
            unique_data = []
            for item in data:
                name = item['Reservationuser']['user']['username']
                if name not in nu_names:
                    nu_names.add(name)
                    unique_data.append(item)
            return response.Response(unique_data, status=status.HTTP_200_OK)
        except:
            return response.Response({"message": "There is no appointment"}, status=status.HTTP_404_NOT_FOUND)


class getUserInfoChatAPIView(GenericAPIView):
    permission_classes = ((permissions.IsAuthenticated,))
    authentication_classes = [JWTAuthentication]

    def get(self, request, user_id):
        user = User.objects.get(user_id=user_id)
        requser = reqUser.objects.get(user=user)

        try:
            userData = []
            userNcp = reqUserncpInfoSerializer(requser)
            userData.append(userNcp.data)
            ncpInstance = UserNCPForm.objects.filter(user=requser)
            ncpData = []
            for ncp in ncpInstance:
                serializer = getNCPAnswerserializer(ncp)
                ncpData.append(serializer.data)
            if ncpData == []:
                userData = reqUserncpInfoSerializer(requser)
                userData.append([])
                return response.Response(userData.data)
            else:
                userData.append(ncpData)
                return response.Response(userData)
        except:
            userData = []
            userNcp = reqUserncpInfoSerializer(requser)
            userData.append(userNcp.data)
            userData.append([])
            return response.Response(userData)


class getUserNCPInfoAPIView(GenericAPIView):
    permission_classes = ((permissions.IsAuthenticated,))
    authentication_classes = [JWTAuthentication]

    def get(self, request):

        requser = reqUser.objects.get(user=request.user)

        try:

            ncpInstance = UserNCPForm.objects.filter(user=requser)
            ncpData = []
            for ncp in ncpInstance:
                serializer = getNCPAnswerserializer(ncp)
                ncpData.append(serializer.data)

            return response.Response(ncpData, status=status.HTTP_200_OK)

        except:

            return response.Response(status=status.HTTP_400_BAD_REQUEST)
