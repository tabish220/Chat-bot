from django.db import models


class User(models.Model):
    email = models.EmailField(unique=True,max_length=50)
    password = models.CharField(max_length=50,blank=False,null=False)
    phone_number = models.CharField(max_length=15,blank=False,null=False)
    city = models.CharField(max_length=50,blank=False,null=False)
    is_admin = models.BooleanField(default=False)



