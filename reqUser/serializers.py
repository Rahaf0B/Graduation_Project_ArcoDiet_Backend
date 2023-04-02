from rest_framework import serializers
from .models import User,Diseases,Allergies,reqUser,Nutritionist




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



class UserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=120,min_length=6,write_only=True)

    class Meta:
        model = User
        fields = ('username','email', 'password','token')
        read_only_fields=['token','username']




class RegisterReqUserSerializer(serializers.ModelSerializer):

    user=UserSerializer(required=True)
    class Meta:
        model=reqUser
        fields=('user',"req_user_first_name","req_user_last_name","gender","age")#,'token') #"allergies","diseases","userweight","height","profile_pic",
    def create(self,validated_data):
        print(validated_data)
       
        user=User.objects.create_user(username=validated_data['req_user_first_name'],email=validated_data['user']['email'],password=validated_data['user']['password'],is_reqUser=True,is_Nutritionist=False)
        userFname=validated_data.pop('req_user_first_name')
        requser=reqUser.objects.create(user=user,req_user_first_name=userFname,req_user_last_name=validated_data.pop('req_user_last_name'),age=validated_data.pop('age'),gender=validated_data.pop('gender'))
        return requser
    
    
class RegisterNutritionistSerializer(serializers.ModelSerializer):

    user=UserSerializer(required=True)
    class Meta:
        model=Nutritionist
        fields=('user',"nutritionist_first_name","nutritionist_last_name","gender","age","phone_number") #"allergies","diseases","userweight","height","profile_pic",
    def create(self,validated_data):
        print(validated_data)
       
        user=User.objects.create_user(username=validated_data['nutritionist_first_name'],email=validated_data['user']['email'],password=validated_data['user']['password'],is_reqUser=False,is_Nutritionist=True)
    
        NutritionistUser=Nutritionist.objects.create(user=user,nutritionist_first_name=validated_data.pop('nutritionist_first_name'),nutritionist_last_name=validated_data.pop('nutritionist_last_name'),age=validated_data.pop('age'),gender=validated_data.pop('gender'),phone_number=validated_data.pop('phone_number'))
        return NutritionistUser
    



    

class AddInformationSerializer(serializers.ModelSerializer):
   

    class Meta:
        model=reqUser
        fields=("allergies","diseases","weight","height")

    def update(self, instance, validated_data):
       
        
        allergies= validated_data.pop('allergies')
        diseases= validated_data.pop('diseases')
        userweight= validated_data.pop('weight', None)
        height= validated_data.pop('height', None)
        instance.weight=userweight
        instance.height=height
        instance.save()

        for alerg in allergies:
            instance.allergies.add(alerg)

        for diss in diseases:
            instance.diseases.add(diss)
        return super().update(instance, validated_data) #AddInformationSerializer,self



class LoginSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=120,min_length=6,write_only=True)
    class Meta():
        model=User
        fields=('email','password','token')
        read_only_fields=['token']


class UserEmailNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email','username')



class UserDataSerializer(serializers.ModelSerializer):
    user=UserEmailNameSerializer()
 

    class Meta:
        model = reqUser
        fields=("user","req_user_first_name","req_user_last_name","gender","age","allergies","diseases","weight","height") 


class NutritionistDataSerializer(serializers.ModelSerializer):
    user=UserEmailNameSerializer()
    class Meta:
        model = Nutritionist
        fields=("user","nutritionist_first_name","nutritionist_last_name","gender","age","phone_number")

class UserIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=('user_id',)




class AllergiesDiseasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=("allergies","diseases")






