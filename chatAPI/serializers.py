from rest_framework import serializers
from .models import Massage

class getMessagesSerializer(serializers.ModelSerializer):

    class Meta:
        model=Massage
        
        fields =['sender','receiver','massage','image','timestamp','type']

        