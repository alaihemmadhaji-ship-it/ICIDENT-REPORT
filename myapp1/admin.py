import IncidentReport
from django.contrib import admin
from .models import *
admin.site.register(User)
admin.site.register(Incident)
admin.site.register(IncidentReport)
admin.site.register(IncidentHistory)

# Register your models here.
