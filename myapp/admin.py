from distutils.command.register import register

from django.contrib import admin
from myapp.models import *
from myapp.views import registration

# Register your models here.
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Ward)
admin.site.register(Appointment1)
admin.site.register(Contact)



