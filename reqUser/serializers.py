from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):

    password=serializers.CharField(max_length=120,min_length=6,write_only=True)
    class Meta():
        model=User
        fields=('email',"first_name","last_name","allergies","diseases","weight","weight","height","age","profile_pic",'password')


    def create(self,validated_data):
        return User.objects.create_user(username=str(validated_data["first_name"]) + str(validated_data["last_name"]),**validated_data)
    

