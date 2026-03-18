# Create your models here.
from django.db import models
from django.contrib.auth.models import User
import random

# from django.db import models

class EmailOTP(models.Model):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    

    

# class Program(models.Model):
#     name = models.CharField(max_length=50,unique=True)

#     def __str__(self):
#         return self.name


# class Semester(models.Model):
#     program = models.ForeignKey(Program, on_delete=models.CASCADE)
#     name = models.CharField(max_length=50)
#     class Meta:
#         unique_together=('program','name')
#     def __str__(self):
#         return f"{self.program.name} - {self.name}"
    
# class Subject(models.Model):
#     semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)

# class Note(models.Model):
#     semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE,null=True, blank=True)
#     title = models.CharField(max_length=200)
#     file = models.FileField(upload_to="notes/")
#     uploaded_at = models.DateTimeField(auto_now_add=True)
#     uploaded_by = models.ForeignKey(
#         User,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True
#     )
    
#     def __str__(self):
#         return self.title
    
from django.conf import settings
from django.core.files.storage import default_storage
def get_signed_url(file_field):
    return default_storage.url(file_field.name)