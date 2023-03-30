from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import RegisterSerializer,LoginSerializer,UsersSerializer,AllergiesDiseasesSerializer,AddInformationSerializer,AddDiseasesSerializer,AddAllergiesSerializer,UserIDSerializer
from rest_framework import response,status,permissions
from django.contrib.auth import authenticate
from .jwt import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from .models import User,Diseases,Allergies
from rest_framework import viewsets
from rest_framework import generics


# Create your views here.


class RegisterAPIView(GenericAPIView):
    serializer_class=RegisterSerializer
    parser_classes = (MultiPartParser, FormParser)    
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data,status=status.HTTP_201_CREATED)
    
        return response.Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    




class AddInformationAPIView(generics.UpdateAPIView):
     
    queryset = User.objects.all()
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
    serializer_class=UsersSerializer
    def get(self,request):
        user=request.user

        serializer=UsersSerializer(user)
        
        return response.Response({'user':serializer.data})



class GetUserIDAPIView(GenericAPIView):
    
    permission_classes=((permissions.IsAuthenticated,))
    authentication_classes=[JWTAuthentication]
    serializer_class=UserIDSerializer

    def get(self,request):
        user=request.user
        serializer=UserIDSerializer(user)
        return response.Response({'user_id':serializer.data})





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
    serializer_class=AddAllergiesSerializer
    def get(self,request):
        queryset=Allergies.objects.all()
        serializer = AddAllergiesSerializer(queryset,many=True)
        return response.Response(serializer.data)
       



class getAllDiseasesAPIView(GenericAPIView):
    serializer_class=AddDiseasesSerializer
    def get(self,request):
        queryset=Diseases.objects.all()
        serializer = AddDiseasesSerializer(queryset,many=True)
        return response.Response(serializer.data)





