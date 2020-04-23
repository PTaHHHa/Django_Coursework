from django.contrib import admin
from Bank.forms import ProfileAdmin, AccountAdmin, DepositAdmin, UserAdmin
from Bank.models import Profile, City, Citizenship, Account, Deposits
from django.contrib.auth.admin import User
# Register your models here.

admin.site.register(City)
admin.site.register(Citizenship)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Deposits, DepositAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

