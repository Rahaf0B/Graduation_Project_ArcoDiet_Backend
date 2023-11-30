from django.db import models
from reqUser.models import User
from django.utils.translation import gettext_lazy as _


class Massage(models.Model):  
    massage_id = models.IntegerField( primary_key=True)
    sender= models.ForeignKey(User,on_delete=models.CASCADE, related_name="sender")
    receiver= models.ForeignKey(User,on_delete=models.CASCADE, related_name="receiver")
    massage=models.CharField(_("massage"), max_length=300, blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/', blank=True,null=True,default='')
    type=models.CharField(_("type"), max_length=50, blank=True,null=True)

    class Meta:
        ordering = ['-timestamp']


class UploadedImage(models.Model):
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)