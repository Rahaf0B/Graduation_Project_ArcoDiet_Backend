from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import RegisterReqUserSerializer,LoginSerializer,UserDataSerializer,AllergiesDiseasesSerializer,AddInformationSerializer,AddDiseasesSerializer,AddAllergiesSerializer,UserIDSerializer,RegisterNutritionistSerializer,NutritionistDataSerializer
from rest_framework import response,status,permissions
from django.contrib.auth import authenticate
from .jwt import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from .models import User,Diseases,Allergies,reqUser,Nutritionist
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework import generics

# Create your views here.


class RegisterReqUserAPIView(GenericAPIView):
    serializer_class=RegisterReqUserSerializer
    parser_classes = (MultiPartParser, FormParser)
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return response.Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    



class RegisterNutritionistUserAPIView(GenericAPIView):
    serializer_class=RegisterNutritionistSerializer
    parser_classes = (MultiPartParser, FormParser)
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return response.Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class AddInformationAPIView(generics.UpdateAPIView):
     
    queryset = reqUser.objects.all()
    serializer_class=AddInformationSerializer
    permission_classes=((permissions.IsAuthenticated,))
    authentication_classes=[JWTAuthentication]
    lookup_field = 'user_id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer=self.serializer_class(instance,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return response.Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(GenericAPIView):

    serializer_class=LoginSerializer
    
    def post(self,request):
        email=request.data.get('email',None)
        password=request.data.get('password',None)
        user=authenticate(username=email,password=password)
        if user:
            serializer=self.serializer_class(user)
            return response.Response(serializer.data,status=status.HTTP_200_OK)
        return response.Response('message:Invalid credentialsm try again',status=status.HTTP_401_UNAUTHORIZED)


class AuthUserAPIView(GenericAPIView):
    permission_classes=((permissions.IsAuthenticated,))
    authentication_classes=[JWTAuthentication]
    serializer_class=UserDataSerializer

    def get(self,request):
        user=request.user
        requ=reqUser.objects.get(user=user)
        serializer=UserDataSerializer(requ)
        
        return response.Response({'user':serializer.data})
    
class AuthNutritionistAPIView(GenericAPIView):
    permission_classes=((permissions.IsAuthenticated,))
    authentication_classes=[JWTAuthentication]
    serializer_class=NutritionistDataSerializer

    def get(self,request):
        user=request.user
        NutritionistUser=Nutritionist.objects.get(user=user)
        serializer=NutritionistDataSerializer(NutritionistUser)
        print(serializer.data)
        
        return response.Response({'user':serializer.data})
    

class GetUserIDAPIView(GenericAPIView):
    
    permission_classes=((permissions.IsAuthenticated,))
    authentication_classes=[JWTAuthentication]
    serializer_class=UserIDSerializer

    def get(self,request):
        user=request.user
        print(user)
        serializer=UserIDSerializer(user)
        return response.Response({'user_id':serializer.data})



class AlergiesDiseasesAPIView(GenericAPIView):

    authentication_classes=[]
    serializer_class=AllergiesDiseasesSerializer

    def get(self,request):
        email=request.data.get('email',None)
        user=request.user
        serializer=AllergiesDiseasesSerializer(user)
        return response.Response({'user':serializer.data})
    


class AddAllergiesAPIView(GenericAPIView):

    serializer_class=AddAllergiesSerializer
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data,status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class AddDiseasesAPIView(GenericAPIView):
    
    serializer_class=AddDiseasesSerializer

    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data,status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class getAllergiesAPIView(GenericAPIView):
    queryset = Allergies.objects.all()
    serializer_class=AddAllergiesSerializer
    def get(self,request):
        queryset=Allergies.objects.all()
        serializer = AddAllergiesSerializer(queryset,many=True)
        return response.Response(serializer.data)
       


class getAllDiseasesAPIView(GenericAPIView):
    queryset = Diseases.objects.all()
    serializer_class=AddDiseasesSerializer
    def get(self,request):
        queryset=Diseases.objects.all()
        serializer = AddDiseasesSerializer(queryset,many=True)
        return response.Response(serializer.data)


