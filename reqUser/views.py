from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import RegisterReqUserSerializer, LoginSerializer, UserDataSerializer, AllergiesDiseasesSerializer, AddInformationSerializer, AddDiseasesSerializer, AddAllergiesSerializer, UserIDSerializer, RegisterNutritionistSerializer, NutritionistDataSerializer, ForgetPasswordEmailSerializer, ResetPassword, CheckVerificationCodeSerializer, EditReqUserSerializer, EditProfilePictureSerializer, EditEmailUserSerializer, logoutUserSerializer, getNutritionistSerializer, UpdateNutritionistRatingSerializer, EditNutritionistSerializer, getNutritionistInfoSerializer, FavoriteNutritionistsSerializer, EditHealthSerializer, EditNutritionistInfoSerializer, getUserInfoChatSerializer, ChangePassword  # ,RelatoinSerializer
from rest_framework import response, status, permissions
from django.contrib.auth import authenticate, logout
from .jwt import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from .models import User, Diseases, Allergies, reqUser, Nutritionist, FavoriteNutritionists
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework import generics
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from rest_framework.views import APIView
import random
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, authentication_classes


class RegisterReqUserAPIView(GenericAPIView):
    serializer_class = RegisterReqUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterNutritionistUserAPIView(GenericAPIView):
    serializer_class = RegisterNutritionistSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddInformationAPIView(generics.UpdateAPIView):

    queryset = User.objects.all()
    serializer_class = AddInformationSerializer
    permission_classes = ((permissions.IsAuthenticated,))
    authentication_classes = [JWTAuthentication]
    lookup_field = 'user_id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditProfilePictureAPIView(generics.UpdateAPIView):
    serializer_class = EditProfilePictureSerializer
    permission_classes = ((permissions.IsAuthenticated,))
    authentication_classes = [JWTAuthentication]
    lookup_field = 'user_id'
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(
            instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditUserEmailAPIView(generics.UpdateAPIView):
    serializer_class = EditEmailUserSerializer
    permission_classes = ((permissions.IsAuthenticated,))
    authentication_classes = [JWTAuthentication]
    lookup_field = 'user_id'
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(
            instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditUserInformationsAPIView(generics.UpdateAPIView):
    serializer_class = EditReqUserSerializer
    permission_classes = ((permissions.IsAuthenticated,))
    authentication_classes = [JWTAuthentication]
    lookup_field = 'user_id'
    queryset = reqUser.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(
            instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(status=status.HTTP_400_BAD_REQUEST)


class EditHealthInformationsAPIView(generics.UpdateAPIView):
    serializer_class = EditHealthSerializer
    permission_classes = ((permissions.IsAuthenticated,))
    authentication_classes = [JWTAuthentication]
    lookup_field = 'user_id'
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.serializer_class(
            instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(status=status.HTTP_400_BAD_REQUEST)


class EditNutritionistInfoAPIView(generics.UpdateAPIView):
    serializer_class = EditNutritionistInfoSerializer
    permission_classes = ((permissions.IsAuthenticated,))
    authentication_classes = [JWTAuthentication]
    lookup_field = 'user_id'
    queryset = Nutritionist.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class logoutAPIView(GenericAPIView):
    serializer_class = logoutUserSerializer
    permission_classes = ((permissions.IsAuthenticated,))
    authentication_classes = [JWTAuthentication]

    def post(self, request, id):
        user = User.objects.get(user_id=id)
        user.is_online = False
        user.save()
        serializer = self.serializer_class(user)

        return response.Response(serializer.data)


class LoginAPIView(GenericAPIView):

    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        user = authenticate(username=email, password=password)
        if user:
            serializer = self.serializer_class(user)
            user.is_online = True
            user.save()

            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response('message:Invalid credentialsm try again', status=status.HTTP_401_UNAUTHORIZED)


class AuthUserAPIView(GenericAPIView):
    permission_classes = ((permissions.IsAuthenticated,))
    authentication_classes = [JWTAuthentication]
    serializer_class = UserDataSerializer

    def get(self, request):
        user = request.user
        requ = reqUser.objects.get(user=user)
        serializer = UserDataSerializer(requ)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class AuthNutritionistAPIView(GenericAPIView):
    permission_classes = ((permissions.IsAuthenticated,))
    authentication_classes = [JWTAuthentication]
    serializer_class = NutritionistDataSerializer

    def get(self, request):
        user = request.user
        NutritionistUser = Nutritionist.objects.get(user=user)
        serializer = NutritionistDataSerializer(NutritionistUser)

        return response.Response(serializer.data, status=status.HTTP_200_OK)


class getALLNutritionistAPIView(GenericAPIView):

    queryset = Nutritionist.objects.all()
    serializer_class = getNutritionistSerializer

    def get(self, request):
        queryset = Nutritionist.objects.all()
        serializer = getNutritionistSerializer(queryset, many=True)
        return response.Response(serializer.data)


class getHighestNutritionistRatingAPIView(generics.ListAPIView):
    queryset = Nutritionist.objects.all().order_by('-rating')[:5]
    serializer_class = getNutritionistSerializer


class changeNutritionistRatingAPIView(generics.UpdateAPIView):
    permission_classes = ((permissions.IsAuthenticated,))
    authentication_classes = [JWTAuthentication]
    lookup_field = 'user_id'
    queryset = Nutritionist.objects.all()
    serializer_class = UpdateNutritionistRatingSerializer


class getNutritionistInformationAPIView(generics.RetrieveAPIView):
    permission_classes = ((permissions.IsAuthenticated,))
    authentication_classes = [JWTAuthentication]

    def get(self, request, user_id):
        try:
            user = User.objects.get(user_id=user_id)
            nutritionist = Nutritionist.objects.get(user=user)
            serializer = getNutritionistInfoSerializer(nutritionist)
            return response.Response(serializer.data)
        except Nutritionist.DoesNotExist:
            return response.Response({"message": "Nutritionist not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer_class = getNutritionistInfoSerializer


class GetUserIDAPIView(GenericAPIView):

    permission_classes = ((permissions.IsAuthenticated,))
    authentication_classes = [JWTAuthentication]
    serializer_class = UserIDSerializer

    def get(self, request):
        user = request.user
        serializer = UserIDSerializer(user)
        return response.Response(serializer.data)


class AlergiesDiseasesAPIView(GenericAPIView):
    authentication_classes = []
    serializer_class = AllergiesDiseasesSerializer

    def get(self, request):
        email = request.data.get('email', None)
        user = request.user
        serializer = AllergiesDiseasesSerializer(user)
        return response.Response({'user': serializer.data})


class AddAllergiesAPIView(GenericAPIView):

    serializer_class = AddAllergiesSerializer

    def post(self, request):
        try:
            allergies = Allergies.objects.get(
                allergies_name=request.data["allergies_name"])
            return response.Response({"error:This allergies is already added"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddDiseasesAPIView(GenericAPIView):

    serializer_class = AddDiseasesSerializer

    def post(self, request):
        try:
            allergies = Diseases.objects.get(
                diseases_name=request.data["diseases_name"])
            return response.Response({"error:This diseases is already added"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class getAllergiesAPIView(GenericAPIView):
    queryset = Allergies.objects.all()
    serializer_class = AddAllergiesSerializer

    def get(self, request):
        queryset = Allergies.objects.all()
        serializer = AddAllergiesSerializer(queryset, many=True)
        return response.Response(serializer.data)


class getAllDiseasesAPIView(GenericAPIView):
    queryset = Diseases.objects.all()
    serializer_class = AddDiseasesSerializer

    def get(self, request):
        queryset = Diseases.objects.all()
        serializer = AddDiseasesSerializer(queryset, many=True)
        return response.Response(serializer.data)


class ForgotPasswordView(APIView):
    serializer_class = ForgetPasswordEmailSerializer

    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return response.Response({'error': 'No user found with that email address'}, status=400)

        serializer = self.serializer_class(user)
        verificationCode = random.randint(1000, 9999)

        user.verificationCode = verificationCode
        user.save()

        subject = 'Reset Your Password'
        message = f'The following is your verification code :\n {str(verificationCode)}'
        from_email = 'rahafbakeer123@gmail.com'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)

        return response.Response({'success': 'Password reset email sent', 'responseData': serializer.data})


class CheckVerificationCodeAPIView(GenericAPIView):
    serializer_class = CheckVerificationCodeSerializer

    def post(self, request):
        email = request.data.get('email', None)
        verificationCode = request.data.get('verificationCode', None)
        try:
            user = User.objects.get(email=email)
        except:
            return response.Response({'error': 'No user found with that email address'}, status=400)

        if user.verificationCode == verificationCode:
            serializer = self.serializer_class(user)
            return response.Response({'message': 'Correct verification Code'}, status=status.HTTP_200_OK)
        return response.Response({'message': 'Invalid verification Code'}, status=status.HTTP_401_UNAUTHORIZED)


class ResetPasswordAPIView(GenericAPIView):
    serializer_class = ResetPassword

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        instance = User.objects.get(email=email)
        serializer = self.serializer_class(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            return response.Response({'massage': 'reset password done'}, status=status.HTTP_200_OK)
        return response.Response({'massage': 'reset password error'}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPIView(GenericAPIView):
    permission_classes = ((permissions.IsAuthenticated,))
    authentication_classes = [JWTAuthentication]
    serializer_class = ChangePassword

    def post(self, request, *args, **kwargs):
        instance = request.user
        password = request.data.get('old_password', None)
        if (authenticate(username=instance.email, password=password)):
            if request.data["new_password1"] == request.data["new_password2"]:
                serializer = self.serializer_class(
                    instance, data=request.data, partial=True)
                oldpass = request.data.pop("old_password")
                if serializer.is_valid():
                    serializer.save()

                    return response.Response({'massage': 'reset password done'}, status=status.HTTP_200_OK)
            else:
                return response.Response({'massage': ' password notkk match'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return response.Response({'massage': ' password not match'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return response.Response({'massage': 'reset password error'}, status=status.HTTP_400_BAD_REQUEST)


class AddFavoriteNutritionistsAPIView(GenericAPIView):
    permission_classes = ((permissions.IsAuthenticated,))
    authentication_classes = [JWTAuthentication]

    def put(self, request, user_id):
        user = User.objects.get(user_id=user_id)
        nutritionist = Nutritionist.objects.get(user=user)
        requser = request.user
        reqUserinstance = reqUser.objects.get(user=requser)
        try:
            FavoriteNutritionistsInstance = FavoriteNutritionists.objects.get(
                req_user=reqUserinstance)
        except:
            FavoriteNutritionistsInstance = FavoriteNutritionists.objects.create(
                req_user=reqUserinstance)

        FavoriteNutritionistsInstance.nutritionist.add(nutritionist)
        FavoriteNutritionistsInstance.save()
        return response.Response({'success': 'Favorite Nutritionists added.'}, status=status.HTTP_201_CREATED)


class DeleteFavoriteNutritionistsAPIView(GenericAPIView):
    permission_classes = ((permissions.IsAuthenticated,))
    authentication_classes = [JWTAuthentication]

    def put(self, request, user_id):
        user = User.objects.get(user_id=user_id)
        nutritionist = Nutritionist.objects.get(user=user)
        requser = request.user
        reqUserinstance = reqUser.objects.get(user=requser)
        try:
            FavoriteNutritionistsInstance = FavoriteNutritionists.objects.get(
                req_user=reqUserinstance, nutritionist=nutritionist)
            FavoriteNutritionistsInstance.nutritionist.remove(nutritionist)
            FavoriteNutritionistsInstance.save()
        except:
            ...

        return response.Response({'success': 'Favorite Nutritionists deleted.'}, status=status.HTTP_201_CREATED)


class GetAllFavoriteNutritionistsAPIView(GenericAPIView):
    permission_classes = ((permissions.IsAuthenticated,))
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        requser = request.user
        reqUserinstance = reqUser.objects.get(user=requser)
        try:
            FavoriteNutritionistsInstance = FavoriteNutritionists.objects.get(
                req_user=reqUserinstance)
            serializer = FavoriteNutritionistsSerializer(
                FavoriteNutritionistsInstance)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return response.Response({'error': 'There is no Favorite Nutritionists'}, status=status.HTTP_404_NOT_FOUND)


class getUserInfoChatAPIView(GenericAPIView):
    permission_classes = ((permissions.IsAuthenticated,))
    authentication_classes = [JWTAuthentication]

    def get(self, request, user_id):
        user = User.objects.get(user_id=user_id)
        serializer = getUserInfoChatSerializer(user)
        return response.Response({"user": serializer.data})
