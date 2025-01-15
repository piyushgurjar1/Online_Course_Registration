from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
   
    def __str__(self):
        return self.title

class User(models.Model):
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    isAdmin = models.BooleanField(default=False)  

    def __str__(self):
        return self.name  