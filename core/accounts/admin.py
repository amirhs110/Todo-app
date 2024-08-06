from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile
from .forms import CustomUserChangeForm,CustomUserCreationForm

# Register your models here.
class ProfileInline(admin.StackedInline):
    """
    Inline admin descriptor for Profile model.
    This allows the Profile model to be displayed and edited within the User admin page.

    Methods:
        get_queryset: Filters the profile queryset to include only the related profile.
        get_formset: Sets the current user object (parent_obj) to ensure correct filtering in get_queryset.
    """

    model = Profile
    can_delete = False
    extra = 0

    def get_queryset(self, request):
        """
        Filters the profile queryset to include only the profile related to the current user.
        
        """
        qs = super().get_queryset(request)
        # Filter the profile queryset to include only the related profile
        if self.parent_obj:
            return qs.filter(user=self.parent_obj)
        return qs.none()

    def get_formset(self, request, obj=None, **kwargs):
        self.parent_obj = obj
        return super().get_formset(request, obj, **kwargs)

class CustomUserAdmin(UserAdmin):
    model=User
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    list_display=('email', 'is_superuser' , 'is_active', 'is_verified')
    list_filter=('is_superuser' , 'is_active','is_verified')
    search_fields=('email',)
    ordering=('-created_date',)

    fieldsets = (
        ("Authentication", {
            "fields": ("email", "password")}),

        ("Permissions", {
            "fields": ("is_superuser", "is_active", 'is_verified')}),

        ("Group Permissions", {
            "classes": ["collapse"],
            "fields": ("groups", "user_permissions",)}),

        ("Login Date", {
            "fields": ("last_login",)}),
    )

    add_fieldsets = (
        ("Authentication", {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
        ("Permissions", {"fields": ("is_superuser", "is_active", "is_verified")}),
    )

    inlines = (ProfileInline,)

admin.site.register(User,CustomUserAdmin)
admin.site.register(Profile)