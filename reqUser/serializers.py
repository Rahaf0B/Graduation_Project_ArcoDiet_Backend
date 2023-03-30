from rest_framework import serializers
from .models import User







class AddAllergiesSerializer(serializers.ModelSerializer):

    class Meta:
        model=Allergies
        fields=("allergies_name",)
        fields = '__all__'
        

class AddDiseasesSerializer(serializers.ModelSerializer):

    class Meta:
        model=Diseases
        fields=("diseases_name",)
        fields = '__all__'













class RegisterSerializer(serializers.ModelSerializer):

    password=serializers.CharField(max_length=120,min_length=6,write_only=True)
    class Meta():
        model=User
        fields=('email',"first_name","last_name","gender","age",'password','token') #"allergies","diseases","userweight","height","profile_pic",
        read_only_fields=['token']

    def create(self,validated_data):
        return User.objects.create_user(username=str(validated_data["first_name"]) + str(validated_data["last_name"]),**validated_data)
     



class AddInformationSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=("allergies","diseases","weight","height")
    def update(self, instance, validated_data):
        allergies= validated_data.pop('allergies')
        diseases= validated_data.pop('diseases')
        userweight= validated_data.pop('userweight', None)
        height= validated_data.pop('height', None)
        instance.userweight=userweight
        instance.height=height
        instance.save()
        for allergie in allergies:
            instance.allergies.add(allergie)
        for diss in diseases:
            instance.diseases.add(diss)
        return super().update(instance, validated_data) #AddInformationSerializer,self




class LoginSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=120,min_length=6,write_only=True)
    class Meta():
        model=User
        fields=('email','password','token')
        read_only_fields=['token']



class UserIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=('user_id',)
    
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=('username','email',"first_name","last_name","allergies","diseases","weight","weight","height","age","profile_pic")


class AllergiesDiseasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=("allergies","diseases")
