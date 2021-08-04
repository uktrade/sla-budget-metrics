from django.contrib import admin
from .models import Spaces, Applications, Orgs


@admin.register(Orgs)
class orgs_admin(admin.ModelAdmin):
    list_display = ('id', 'org_name', 'org_guid', 'check_enabled')
    #actions = [space_toggle_enabled, ]


@admin.register(Spaces)
class spaces_admin(admin.ModelAdmin):
    list_display = ('id', 'space_name', 'space_guid', 'check_enabled')
    #actions = [space_toggle_enabled, ]


@admin.register(Applications)
class applications_admin(admin.ModelAdmin):
    list_display = ('id',
                    'org_name',
                    'space_name',
                    'app_name',
                    'budget',
                    'budget_left',
                    'budget_reset_date')


    def space_name(self, obj):
        return (obj.spaces.space_name)

    def org_name(self, obj):
        return (obj.spaces.orgs.org_name)
