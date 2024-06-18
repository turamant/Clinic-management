from django.contrib import admin

from accounts.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'birth_date', 'gender', 'address', 'phone')
    list_filter = ('role', 'gender')
    search_fields = ('username', 'email')