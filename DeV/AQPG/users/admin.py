from django.contrib import admin
#from .models import Department
from users.models import *

admin.site.register(Department)
admin.site.register(Profile)


# Register your models here.
