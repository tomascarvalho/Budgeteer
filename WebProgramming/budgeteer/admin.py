from django.contrib import admin

#Register your models here.
from django.contrib.auth.models import User
from .models import Account, Objective, Transaction, User

admin.site.unregister(User)
admin.site.register(User)
admin.site.register(Account)
admin.site.register(Objective)
admin.site.register(Transaction)
