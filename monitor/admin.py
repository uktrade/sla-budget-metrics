from django.contrib import admin
from .models import Spaces, Orgs


@admin.register(Orgs)
class orgs_admin(admin.ModelAdmin):
    list_display = ('id', 'org_name', 'org_guid', 'check_enabled')
    #actions = [space_toggle_enabled, ]


@admin.register(Spaces)
class spaces_admin(admin.ModelAdmin):
    list_display = ('id', 'space_name', 'space_guid', 'check_enabled')
    #actions = [space_toggle_enabled, ]
