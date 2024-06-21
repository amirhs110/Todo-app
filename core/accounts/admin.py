from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import CustomUserChangeForm,CustomUserCreationForm

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model=User
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    list_display=('email', 'is_superuser' , 'is_active')
    list_filter=('is_superuser' , 'is_active')
    search_fields=('email',)
    ordering=('-created_date',)

    fieldsets = (
        ("Authentication", {
            "fields": ("email", "password")}),

        ("User Information", {
            "fields": ("first_name", "last_name")}),

        ("Permissions", {
            "fields": ("is_superuser", "is_active")}),

        ("Group Permissions", {
            "classes": ["collapse"],
            "fields": ("groups", "user_permissions",)}),

        ("Login Date", {
            "fields": ("last_login",)}),
    )

    add_fieldsets = (
        ("Authentication", {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
        ("User Information", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_superuser", "is_active")}),
    )

admin.site.register(User,CustomUserAdmin)