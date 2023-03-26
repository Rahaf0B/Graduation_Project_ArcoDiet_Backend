from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import RegisterSerializer,LoginSerializer,UsersSerializer
from rest_framework import response,status,permissions
from django.contrib.auth import authenticate
from .jwt import JWTAuthentication


# Create your views here.

class RegisterAPIView(GenericAPIView):
    
    serializer_class=RegisterSerializer
    def post(self,request):
        serializer=self.serializer_class(data=request.data)

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

