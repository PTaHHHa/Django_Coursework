from django.contrib import admin
from Bank.forms import ProfileAdmin
from Bank.models import Profile, City, Citizenship
# Register your models here.

admin.site.register(City)
admin.site.register(Citizenship)
admin.site.register(Profile, ProfileAdmin)
