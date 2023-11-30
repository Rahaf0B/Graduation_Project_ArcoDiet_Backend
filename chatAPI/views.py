

from django.db.models import Q

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.generics import GenericAPIView
from .models import Massage, UploadedImage
from .serializers import getMessagesSerializer
from rest_framework import response, status, permissions
from reqUser.jwt import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView


class getAllMSGAPIView(GenericAPIView):
    permission_classes = ((permissions.IsAuthenticated,))
    authentication_classes = [JWTAuthentication]
    queryset = Massage.objects.all()
    serializer_class = getMessagesSerializer

    def get(self, request, receiver):
        user = request.user
        queryset = Massage.objects.filter(
            (Q(sender=user) & Q(receiver=receiver)) | (
                Q(sender=receiver) & Q(receiver=user))
        )
        data = getMessagesSerializer(queryset, many=True, context={
                                     'request': request}).data
        return response.Response(data)


class ImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        image_file = request.FILES.get('image')
        if image_file:
            uploaded_image = UploadedImage.objects.create(image=image_file)
            return response.Response({'message': 'Image uploaded successfully!', 'image_url': uploaded_image.image.url})
        else:
            return response.Response({'error': 'No image file received.'}, status=400)
