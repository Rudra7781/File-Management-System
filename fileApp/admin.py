from django.contrib import admin
from .models import *


admin.site.site_header = "Admin for File Manager"
# Register your models here.


class list_file(admin.ModelAdmin):
    list_display = ['id','name','upload_by']
    list_filter = ['id','name','upload_by']


class list_emp(admin.ModelAdmin):
    list_display = ['id','first_name','dob','emp_email','date_join']
    list_filter = ['id','first_name','dob','emp_email','date_join']

class list_detail(admin.ModelAdmin):
    list_display = ['id','file_to']
    list_filter = ['id','file_to']

admin.site.register(file,list_file)
admin.site.register(employee,list_emp)
admin.site.register(fileDetail,list_detail)

