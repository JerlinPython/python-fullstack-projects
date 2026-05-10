from django.db import models
from django.db.models import CharField


# Create your models here.

class signup(models.Model):
    Name=models.CharField(max_length=100)
    Gmail=models.EmailField()
    Password=models.CharField(max_length=100)

    def __str__(self):
        return self.Name

class basicdata(models.Model):
    Name=models.CharField(max_length=100)
    Age=models.IntegerField()
    Phone=models.CharField(max_length=100)
    Email=models.EmailField()
    Gender=models.CharField(max_length=100)
    Date=models.DateField()

    def __str__(self):
        return self.Name

class educationdata(models.Model):
    Name=models.CharField(max_length=100)
    School=models.CharField(max_length=100)
    Course=models.CharField(max_length=100)
    Degree=models.CharField(max_length=100)
    Resource=models.CharField(max_length=100)

    def __str__(self):
        return self.Name

class financialdata(models.Model):
    Name=models.CharField(max_length=100)
    Bank=models.CharField(max_length=100)
    Account=models.IntegerField()
    Ifsc=models.CharField(max_length=100)

    def __str__(self):
        return self.Name

class employedata(models.Model):
    Name=models.CharField(max_length=100)
    Employeid=models.IntegerField()
    Company=models.CharField(max_length=100)
    Field=models.CharField(max_length=100)
    Experience=models.CharField(max_length=100)

    def __str__(self):
        return  self.Name

class medicaldata(models.Model):
    Name=models.CharField(max_length=100)
    Age=models.IntegerField()
    Height=models.CharField(max_length=100)
    Weight=models.IntegerField()
    Health=models.CharField(max_length=100)

    def __str__(self):
        return self.Name

class filedata(models.Model):
    Name=models.CharField(max_length=100)
    Marksheet=models.FileField()
    Degree=models.FileField()
    Passport=models.FileField()
    Medical=models.FileField()
    Work=models.FileField()

    def __str__(self):
        return self.Name
