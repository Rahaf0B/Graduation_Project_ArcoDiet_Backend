from rest_framework import serializers
from .models import User, Diseases, Allergies, reqUser, Nutritionist, FavoriteNutritionists


class AddAllergiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Allergies
        fields = ("allergies_name",)
        fields = '__all__'


class AddDiseasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diseases
        fields = ("diseases_name",)
        fields = '__all__'


class getAllergiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergies
        fields = ("allergies_name",)


class getDiseasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diseases
        fields = ("diseases_name",)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=120, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ('user_id', 'first_name', 'last_name', 'date_of_birth',
                  'gender', 'username', 'email', 'password', 'age', 'token')
        read_only_fields = ['age', 'token', 'username', 'user_id']


class RegisterReqUserSerializer(serializers.ModelSerializer):

    user = UserSerializer(required=True)

    class Meta:
        model = reqUser
        fields = ('user',)

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['user']['first_name']+" "+validated_data['user']['last_name'], first_name=validated_data['user']['first_name'], last_name=validated_data['user']['last_name'],
                                        date_of_birth=validated_data['user']['date_of_birth'], gender=validated_data['user']['gender'], email=validated_data['user']['email'], password=validated_data['user']['password'], is_reqUser=True, is_Nutritionist=False)

        requser = reqUser.objects.create(user=user)
        return requser


class RegisterNutritionistSerializer(serializers.ModelSerializer):

    user = UserSerializer(required=True)

    class Meta:
        model = Nutritionist
        fields = ('user',)

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['user']['first_name']+" "+validated_data['user']['last_name'], first_name=validated_data['user']['first_name'], last_name=validated_data['user']['last_name'],
                                        date_of_birth=validated_data['user']['date_of_birth'], gender=validated_data['user']['gender'], email=validated_data['user']['email'], password=validated_data['user']['password'], is_reqUser=False, is_Nutritionist=True)

        NutritionistUser = Nutritionist.objects.create(user=user)
        return NutritionistUser


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name',
                  'last_name', 'age', 'email', 'token')
        read_only_fields = ['token', 'username']


class EditProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("profile_pic",)

        def update(self, instance, validated_data):
            instance.user.profile_pic = validated_data.pop("profile_pic")
            instance.user.save()
            instance.save()
            return super().update(instance, validated_data)


class UserEditInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name',
                  'last_name', 'age', 'date_of_birth')
        read_only_fields = ['token', 'username']


class EditReqUserSerializer(serializers.ModelSerializer):
    user = UserEditInfoSerializer(required=True)

    class Meta:
        model = reqUser
        fields = ("user",)

    def update(self, instance, validated_data):
        fname = validated_data['user'].pop('first_name', None)
        lname = validated_data['user'].pop('last_name', None)
        dateOfBirth = validated_data['user'].pop('date_of_birth', None)
        username = instance.user.username
        if (fname != ""):
            instance.user.first_name = fname

        if (lname != ""):
            instance.user.last_name = lname

        if (dateOfBirth != ""):
            instance.user.date_of_birth = dateOfBirth

        instance.user.username = instance.user.first_name+" "+instance.user.last_name

        instance.user.save()
        instance.save()
        super().update(instance.user, validated_data)
        return instance


class UserEditInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name',
                  'last_name', 'age', 'date_of_birth')
        read_only_fields = ['token', 'username']


class EditHealthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("allergies", "diseases", "weight", "height")

    def update(self, instance, validated_data):
        allergies = validated_data.pop('allergies')
        diseases = validated_data.pop('diseases')
        weight = validated_data.pop('weight', None)
        height = validated_data.pop('height', None)

        if (weight != 0):
            instance.weight = weight
        if (height != 0):
            instance.height = height

        instance.allergies.set(allergies)
        instance.diseases.set(diseases)
        instance.save()
        super().update(instance, validated_data)
        return instance


class EditNutritionistInfoSerializer(serializers.ModelSerializer):
    user = UserEditInfoSerializer(required=True)

    class Meta:
        model = Nutritionist
        fields = ("user", "phone_number", "description", "experience_years",
                  "collage", "Specialization", "Price", "rating")
        read_only_fields = ['rating',]

    def update(self, instance, validated_data):
        fname = validated_data['user'].pop('first_name', None)
        lname = validated_data['user'].pop('last_name', None)
        dateOfBirth = validated_data['user'].pop('date_of_birth', None)
        phone_number = validated_data.pop('phone_number', None)
        description = validated_data.pop('description', None)
        experience_years = validated_data.pop('experience_years', None)
        collage = validated_data.pop('collage', None)
        Specialization = validated_data.pop('Specialization', None)
        Price = validated_data.pop('Price', None)

        username = instance.user.username
        if (fname != ""):
            instance.user.first_name = fname

        if (lname != ""):
            instance.user.last_name = lname

        if (dateOfBirth != ""):
            instance.user.date_of_birth = dateOfBirth

        instance.user.username = instance.user.first_name+" "+instance.user.last_name
        if (phone_number != 0 and phone_number != -1 and phone_number != instance.phone_number):
            instance.phone_number = phone_number
        if (description != "" and description != instance.description):
            instance.description = description
        if (experience_years != 0 and experience_years != -1 and experience_years != instance.experience_years):
            instance.experience_years = experience_years
        if (collage != "" and collage != instance.collage):
            instance.collage = collage
        if (Specialization != "" and Specialization != instance.Specialization):
            instance.Specialization = Specialization

        if (Price != 0 and Price != instance.Price and Price != -1):
            instance.Price = Price

        instance.user.save()
        instance.save()
        super().update(instance.user, validated_data)
        return instance


class AddUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("allergies", "diseases", "weight", "height")


class AddInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("allergies", "diseases", "weight", "height")

    def update(self, instance, validated_data):
        allergies = validated_data.pop('allergies')
        diseases = validated_data.pop('diseases')
        userweight = validated_data.pop('weight', None)
        height = validated_data.pop('height', None)
        instance.weight = userweight
        instance.height = height

        for alerg in allergies:
            instance.allergies.add(alerg)

        for diss in diseases:
            instance.diseases.add(diss)
        instance.save()
        return super().update(instance, validated_data)


class EditEmailUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'token')
        read_only_fields = ['token', 'username']

        def update(self, instance, validated_data):
            email = validated_data.pop('email')
            if (email != "" or email != instance.email):
                instance.user.email = email
                instance.user.save()
                instance.save()
                return super().update(instance, validated_data)
            return instance


class NutritionistUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("user_id", "username", "profile_pic")


class getNutritionistSerializer(serializers.ModelSerializer):
    user = NutritionistUserInfoSerializer(required=True)

    class Meta:
        model = Nutritionist
        fields = ("user", "rating", "Price")


class getNutritionistInfoSerializer(serializers.ModelSerializer):
    user = NutritionistUserInfoSerializer(required=True)

    class Meta:
        model = Nutritionist
        fields = ("user", "rating", "Price", "description", "experience_years")


# NOT USED
class EditNutritionistSerializer(serializers.ModelSerializer):
    user = UserEditSerializer(required=True)

    class Meta:
        model = Nutritionist
        fields = ("user", "Price", "phone_number", "description",
                  "experience_years", "collage", "Specialization")

    def update(self, instance, validated_data):
        fname = validated_data['user'].pop('first_name', None)
        lname = validated_data['user'].pop('last_name', None)
        age = validated_data['user'].pop('age', None)
        phone_number = validated_data.pop('phone_number')
        description = validated_data.pop('description')
        experience_years = validated_data.pop('experience_years')
        collage = validated_data.pop('collage')
        Specialization = validated_data.pop('Specialization')
        Price = validated_data.pop('Price')
        username = instance.user.username
        if (fname != ""):
            instance.user.first_name = fname

        if (lname != ""):
            instance.user.last_name = lname
        if (Price != 0):
            instance.Price = Price
        if (age != 0):
            instance.user.age = age
        if (phone_number != 0):
            instance.phone_number = phone_number
        if (experience_years != -1):
            instance.experience_years = experience_years
        if (description != ""):
            instance.description = description
        if (collage != ""):
            instance.collage = collage
        if (Specialization != ""):
            instance.Specialization = Specialization
        instance.user.username = instance.user.first_name+" "+instance.user.last_name

        instance.user.save()
        instance.save()
        return super().update(instance, validated_data)


class logoutUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('is_active', 'token')
        read_only_fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=120, min_length=6, write_only=True)

    class Meta():
        model = User
        fields = ('email', 'password', 'is_reqUser',
                  'is_Nutritionist', 'token')
        read_only_fields = ['token']


class UserEmailNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')


class GetUserDataSerializer(serializers.ModelSerializer):
    allergies = getAllergiesSerializer(required=True, many=True)
    diseases = getDiseasesSerializer(required=True, many=True)

    class Meta:
        model = User
        fields = ('user_id', 'email', 'first_name', 'last_name', 'username', 'date_of_birth',
                  'age', 'gender', "allergies", "diseases", "weight", "height", 'profile_pic')


class UserDataSerializer(serializers.ModelSerializer):
    user = GetUserDataSerializer()

    class Meta:
        model = reqUser
        fields = ("user",)


class NutritionistDataSerializer(serializers.ModelSerializer):
    user = GetUserDataSerializer()

    class Meta:
        model = Nutritionist
        fields = ("user", "phone_number", "rating", "description",
                  "experience_years", "collage", "Specialization", "Price")


class UserIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id',)


class AllergiesDiseasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("allergies", "diseases")


class ForgetPasswordEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'verificationCode')
        read_only_fields = ['verificationCode',]


class CheckVerificationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'verificationCode')


class ResetPassword(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'new_password1', 'new_password2')
    new_password1 = serializers.CharField(required=False)
    new_password2 = serializers.CharField(required=False)

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError(
                "the two password is not the same")
        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password1'])
        instance.save()
        return instance


class ChangePassword(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('new_password1', 'new_password2')
    new_password1 = serializers.CharField(required=False)
    new_password2 = serializers.CharField(required=False)

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError(
                "the two password is not the same")
        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password1'])
        instance.save()
        return instance


class userReservationAppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = User


class UpdateNutritionistRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutritionist
        fields = ['rating']


class FavoriteNutritionistsSerializer(serializers.ModelSerializer):
    nutritionist = getNutritionistSerializer(required=True, many=True)

    class Meta:
        model = FavoriteNutritionists
        fields = ('nutritionist',)


class getUserInfoChatSerializer(serializers.ModelSerializer):

    allergies = getAllergiesSerializer(required=True, many=True)
    diseases = getDiseasesSerializer(required=True, many=True)

    class Meta:
        model = User
        fields = ("username", "profile_pic", "allergies",
                  "diseases", "weight", "height")
