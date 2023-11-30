from django.db import models
from reqUser.models import User
from django.utils.translation import gettext_lazy as _
from reqUser.models import User, reqUser

# Create your models here.


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    barcode_number = models.IntegerField(
        _("barcode_number"), blank=True, null=True)
    product_name_english = models.CharField(
        _("product_name_english"), max_length=100, blank=True, null=True)
    product_name_arabic = models.CharField(
        _("product_name_arabic"), max_length=100, blank=True, null=True)
    product_weight = models.FloatField(
        _("product_weight"), blank=True, null=True)
    sugar_value = models.FloatField(_("sugar_value"), blank=True, null=True)
    sodium_value = models.FloatField(_("sodium_value"), blank=True, null=True)
    calories_value = models.FloatField(
        _("calories_value"), blank=True, null=True)
    fats_value = models.FloatField(_("fats_value"), blank=True, null=True)
    protein_value = models.FloatField(
        _("protein_value"), blank=True, null=True)
    cholesterol_value = models.FloatField(
        _("cholesterol_value"), blank=True, null=True)
    carbohydrate_value = models.FloatField(
        _("carbohydrate_value"), blank=True, null=True)
    milk_existing = models.IntegerField(
        _("milk_existing"), blank=True, null=True)
    egg_existing = models.IntegerField(
        _("egg_existing"), blank=True, null=True)
    fish_existing = models.IntegerField(
        _("fish_existing"), blank=True, null=True)
    sea_components_existing = models.IntegerField(
        _("sea_components_existing"), blank=True, null=True)
    nuts_existing = models.IntegerField(
        _("nuts_existing"), blank=True, null=True)
    peanut_existing = models.IntegerField(
        _("peanut_existing"), blank=True, null=True)
    pistachio_existing = models.IntegerField(
        _("pistachio_existing"), blank=True, null=True)
    wheat_derivatives_existing = models.IntegerField(
        _("wheat_derivatives_existing"), blank=True, null=True)
    soybeans_existing = models.IntegerField(
        _("soybeans_existing"), blank=True, null=True)


class FavoriteProducts(models.Model):
    Favorite_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="UserInstance")
    product = models.ManyToManyField(Product, related_name="FavoriteProduct")
