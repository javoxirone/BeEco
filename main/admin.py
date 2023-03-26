from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin


class ProfileImageInline(admin.TabularInline):
    fk_name = 'user'
    model = ProfileImage
    extra = 1


class UserBadgeInline(admin.TabularInline):
    fk_name = 'user'
    model = UserBadge
    extra = 0


class UserAdmin(AuthUserAdmin):
    inlines = [ProfileImageInline, UserBadgeInline]


# Register your models here.
admin.site.register(Category)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Venue)
admin.site.register(Waste)
admin.site.register(Recommendation)
admin.site.register(MeasurementUnit)
admin.site.register(Badge)
