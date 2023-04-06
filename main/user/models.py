from django.db import models


# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=250)
    image = models.CharField(max_length=250)


class ProductUser(models.Model):
    user_id = models.IntegerField()
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
