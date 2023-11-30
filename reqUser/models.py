from django.db import models
from django.db import models
from django.contrib.auth.models import (
    PermissionsMixin, UserManager, AbstractBaseUser)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.apps import apps
from django.contrib.auth.hashers import make_password
import jwt
from datetime import date, datetime, timedelta

from django.conf import settings


class MyUserManager(UserManager):
    def _create_user(self, username,  email, password, **extra_fields):

        if not username:
            raise ValueError("The given username must be set")

        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )

        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)


class Allergies(models.Model):

    allergies_id = models.AutoField(primary_key=True)
    allergies_name = models.CharField(
        _("allergies_name"), max_length=150, blank=True, null=True)

    def __str__(self):
        return self.allergies_name


class Diseases(models.Model):

    diseases_id = models.AutoField(primary_key=True)
    diseases_name = models.CharField(
        _("diseases_name"), max_length=150, blank=True, null=True)

    def __str__(self):
        return self.diseases_name


def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)


class User(AbstractBaseUser, PermissionsMixin, models.Model):

    user_id = models.AutoField(primary_key=True)

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        validators=[username_validator]
    )

    is_reqUser = models.BooleanField(default=False)
    is_Nutritionist = models.BooleanField(default=False)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    is_online = models.BooleanField(
        _("is_online"),
        default=True,)

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    email = models.EmailField(
        _("email address"), blank=False, unique=True, null=True)
    verificationCode = models.CharField(_("verificationCode"), max_length=10)

    first_name = models.CharField(
        _("first_name"), max_length=150, blank=True, null=True)
    last_name = models.CharField(
        _("last_name"), max_length=150, blank=True, null=True)
    gender = models.CharField(_("gender"), max_length=5, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    # age=models.IntegerField(blank=True,null=True)
    profile_pic = models.ImageField(upload_to='images/', blank=True, null=True)
    date_of_birth = models.DateField(_("date_of_birth"), blank=True, null=True)
    allergies = models.ManyToManyField(
        Allergies, blank=True, null=True, related_name="Allergies")
    diseases = models.ManyToManyField(
        Diseases, blank=True, null=True, related_name="Disease")
    weight = models.FloatField(_("weight"), blank=True, null=True)
    height = models.FloatField(_("height"), blank=True, null=True)

    objects = MyUserManager()
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    @property
    def age(self):
        todayDate = date.today()
        return todayDate.year - self.date_of_birth.year - ((todayDate.month, todayDate.day) < (self.date_of_birth.month,  self.date_of_birth.day))

    @property
    def token(self):
        if self.is_online:
            token = jwt.encode({'email': self.email, 'exp': datetime.utcnow() + timedelta(days=30), 'logout': False},
                               settings.SECRET_KEY, algorithm='HS256')
            return token
        else:
            return None

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = str(self.first_name) + " " + str(self.last_name)
        super().save(*args, **kwargs)

    def __str__(self):

        return str(self.username)


class reqUser(models.Model):

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="reqUser")

    def __str__(self):

        return str(self.user.first_name) + " " + str(self.user.last_name)


class Nutritionist(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="Nutritionist")
    phone_number = models.IntegerField(
        _("phone_number"), blank=True, null=True)
    rating = models.IntegerField(_("rating"), blank=True, null=True)
    description = models.CharField(
        _("description"), max_length=500, blank=True, null=True)
    experience_years = models.IntegerField(
        _("experience_yaer"), blank=True, null=True)
    collage = models.CharField(
        _("collage"), max_length=100, blank=True, null=True)
    Specialization = models.CharField(
        _("Specialization"), max_length=100, blank=True, null=True)
    Price = models.IntegerField(_("Price"), blank=True, null=True)

    def __str__(self):

        return str(self.user.first_name) + " " + str(self.user.last_name)


class FavoriteNutritionists(models.Model):
    Favorite_id = models.AutoField(primary_key=True)
    req_user = models.ForeignKey(
        reqUser, on_delete=models.CASCADE, related_name="reqUserInstance")
    nutritionist = models.ManyToManyField(
        Nutritionist, related_name="FavoriteNutritionists")
