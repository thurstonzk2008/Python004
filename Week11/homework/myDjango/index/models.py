from django.db import models

# Create your models here.

class Type(models.Model):
    id = models.AutoField(primary_key=True)
    typename = models.CharField(max_length=20)


class Name(models.Model):
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    starts = models.CharField(max_length=50)
