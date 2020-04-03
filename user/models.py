from django.db import models

# Create your models here.

class User(models.Model):
    u_name = models.CharField(max_length=20)
    u_password = models.CharField(max_length=225)
    u_ticket = models.CharField(max_length=30,null=True)

    class Meta:
        db_table = 'mysite_user'