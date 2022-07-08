from distutils.command.upload import upload
from email.policy import default
import imp
from django.db import models
from django.contrib.auth.models import User,auth


# Create your models here.


class employee(models.Model):

    DEPARTMENT = (
        ('I.T', 'IT'),
        ('H.R', 'HR'),
    )

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    emp_email = models.EmailField()
    emp_pass = models.CharField(max_length=25)
    phone = models.IntegerField()
    dept = models.CharField(max_length = 10,choices=DEPARTMENT)
    dob = models.DateField()
    img = models.ImageField(upload_to='user',default='')
    date_join = models.DateField()


    def __str__(self):
        return self.first_name

class file(models.Model):
    name = models.CharField(max_length=20)
    desc = models.TextField()
    file = models.FileField(upload_to='file')
    upload_at = models.DateField()
    upload_by = models.ForeignKey(employee,on_delete=models.CASCADE,default='')


    def __str__(self):
        return self.name

class fileDetail(models.Model):
    file_to = models.ForeignKey(file,on_delete=models.CASCADE)
    given_to = models.ManyToManyField(employee,related_name='person',blank=True)
    approved_by = models.ManyToManyField(employee,related_name='personYes',blank=True)
    rejected_by = models.ManyToManyField(employee,related_name='personNo',blank=True)

    def __str__(self):
        return str(self.file_to.name)
    