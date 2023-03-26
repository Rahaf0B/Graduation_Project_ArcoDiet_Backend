from django.db import models
from django.db import models
from django.contrib.auth.models import (PermissionsMixin,UserManager,AbstractBaseUser)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.apps import apps
from django.contrib.auth.hashers import make_password
import jwt
from datetime import datetime, timedelta

from django.conf import settings






class MyUserManager(UserManager):
    def _create_user(self,username,  email, password, **extra_fields):
       
        if not username:
            raise ValueError("The given username must be set")

        if not email:
            raise ValueError("The given eamil must be set")
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
                
        
        username = GlobalUserModel.normalize_username(username)
        user = self.model( email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self,username,email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self,username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user( username,email, password, **extra_fields)



class User(AbstractBaseUser,PermissionsMixin,models.Model):
    username_validator = UnicodeUsernameValidator()   
    username=models.CharField(
        _('username'),
        max_length=150,
        validators=[username_validator]
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=True,null=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True,null=True)
    allergies=models.CharField(_("allergies"), max_length=150, blank=True,null=True)
    diseases=models.CharField(_("diseases"), max_length=150, blank=True,null=True)
    weight=models.FloatField(_("weight"),blank=True,null=True)
    height=models.FloatField(_("height"),blank=True,null=True)
    email = models.EmailField(_("email address"), blank=False,unique=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=True,null=True)
    age=models.IntegerField(blank=True,null=True)
    profile_pic=models.ImageField(upload_to='image',blank=True,null=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    email_verified= models.BooleanField(
        _("email_verified"),
        default=False,
        help_text=_(
            "Designates whether this users email verfied"
        
        ),
    )
    objects = MyUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name","last_name","allergies","diseases","weight","weight","height","age"]


    
    def save(self,*args,**kwargs):
        self.username = str(self.first_name) + str(self.last_name)
        super().save(*args , **kwargs)


    @property
    def token(self):
        token=jwt.encode({'email':self.email,'exp':datetime.utcnow()+ timedelta(hours=24)},
                         settings.SECRET_KEY,algorithm='HS256')
    

        return token


