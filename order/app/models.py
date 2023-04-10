from django.db import models


# Create your models here.
class OderedProducts(models.Model):
    user_id = models.IntegerField()
    product_id = models.IntegerField()
    product_tittle = models.CharField(max_length=255)
