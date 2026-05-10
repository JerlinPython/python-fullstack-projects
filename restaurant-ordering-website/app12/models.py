from django.db import models

# Create your models here.

class signup(models.Model):
    Username=models.CharField(max_length=100)
    Email=models.EmailField(null=True,blank=True)
    Password=models.CharField(max_length=100)
    Phone=models.CharField(max_length=100)
    Address=models.CharField(max_length=100)

    def __str__(self):
        return self.Username

class reserv(models.Model):
    Firstname=models.CharField(max_length=100)
    Date=models.DateField()
    Time=models.TimeField()
    People=models.IntegerField()
    Phone=models.IntegerField()

    def __str__(self):
        return self.Firstname


class Foodtable(models.Model):
    Foodname=models.CharField(max_length=100)
    Image = models.FileField()
    Quantity=models.IntegerField()
    Unitprice=models.IntegerField()
    Brand = models.CharField(max_length=100)
    Description = models.CharField(max_length=10000)
    def __str__(self):
        return self.Foodname

class Carttable(models.Model):
    Productid = models.IntegerField()
    Foodname = models.CharField(max_length=100)
    Quantity = models.IntegerField()
    price = models.IntegerField()
    Userid = models.CharField(max_length=100)

    def __str__(self):
        return self.Foodname

class Billtable(models.Model):
    Productid = models.IntegerField()
    Foodname = models.CharField(max_length=100)
    Quantity = models.IntegerField()
    price = models.IntegerField()
    Userid = models.CharField(max_length=100)
    Firstname = models.CharField(max_length=100)

    def __str__(self):
        return self.Foodname