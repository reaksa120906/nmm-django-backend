from django.contrib import admin
from .models import UserProfile, Expense, Income, Savings

admin.site.register(UserProfile)
admin.site.register(Expense)
admin.site.register(Income)
admin.site.register(Savings)
