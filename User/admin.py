from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from User.models import User
from .forms import CreateUserForm
from django.utils.translation import ngettext
from django.contrib import messages
# Register your models here.


fields = list(UserAdmin.fieldsets)
fields[1] = (
    'Personal Info', {
        'fields': (
            'first_name', 'last_name', 'email', 'image',
        )
    })


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("is_active",)
    add_form = CreateUserForm
    fieldsets = UserAdmin.fieldsets + (
        'Personal Info', {
            'fields': (
                'first_name', 'last_name', 'email', 'image',
            )
        })
    fieldsets = tuple(fields)
    actions = ('make_users_inactive', 'make_users_active',)

    @admin.action(description='make selected users disabled')
    def make_users_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            ngettext(
                f'{updated} user was successfully marked as unactive',
                f'{updated} users were successfully marked as unactive',
                updated
            ),
            messages.SUCCESS


        )

    @admin.action(description='make selected users active')
    def make_users_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            ngettext(
                f'{updated} user was successfully marked as active',
                f'{updated} users were successfully marked as active',
                updated
            ),
            messages.SUCCESS


        )
