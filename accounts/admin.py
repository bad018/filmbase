from django.contrib import admin
from .models import UserWithAccount


@admin.register(UserWithAccount)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'birthday', 'avatar', 'address', 'bio']
    raw_id_fields = ['user']
