from django.contrib import admin
from Bank.forms import ProfileAdmin, AccountAdmin, DepositAdmin
from Bank.models import Profile, City, Citizenship, Account, Deposits
# Register your models here.

admin.site.register(City)
admin.site.register(Citizenship)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Deposits, DepositAdmin)
