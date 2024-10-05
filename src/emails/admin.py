from django.contrib import admin
from .models import Email, EmailVerification


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ['email']
    fields = ['email', 'active']

@admin.register(EmailVerification)
class EmailAdmin(admin.ModelAdmin):
    list_display = ['parent__email', 'email']