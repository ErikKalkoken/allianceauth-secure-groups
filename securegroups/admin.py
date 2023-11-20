from django.contrib import admin
from django.utils.html import format_html

# Register your models here.
from .models import (
    GracePeriodRecord,
    GroupUpdateWebhook,
    SmartGroup,
    SmartFilter,
    AltCorpFilter,
    AltAllianceFilter,
    UserInGroupFilter
)


class GraceAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ["group", "user", "grace_filter", "expires"]
    search_fields = ["group__group__name", "user__username"]
    list_filter = ["grace_filter"]

    def user_name(self, obj):
        return obj.user.username

    user_name.short_description = "User"
    user_name.admin_order_field = "user__username"

    def group_name(self, obj):
        return obj.group.group.name

    group_name.short_description = "Group"
    group_name.admin_order_field = "group__group__name"


admin.site.register(GracePeriodRecord, GraceAdmin)


class SmartfilterAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    list_display = ["__str__", "grace_period"]


admin.site.register(SmartFilter, SmartfilterAdmin)


class SmartGroupAdmin(admin.ModelAdmin):
    filter_horizontal = ["filters"]
    list_display = ["__str__", "enabled", "auto_group",
                    "include_in_updates", "can_grace"]


admin.site.register(SmartGroup, SmartGroupAdmin)


class AltCorpAdmin(admin.ModelAdmin):
    list_select_related = ["alt_corp"]
    list_display = ["__str__", "alt_corp"]
    raw_id_fields = ["alt_corp"]
    filter_horizontal = ["exempt_alliances", "exempt_corporations"]


admin.site.register(AltCorpFilter, AltCorpAdmin)


class UserInGroupFilterAdmin(admin.ModelAdmin):
    list_display = ["__str__", "_groups", "reversed_logic"]
    filter_horizontal = ["groups", "exempt_alliances", "exempt_corporations"]

    def _list_2_html_w_tooltips(self, my_items: list, max_items: int) -> str:
        """converts list of strings into HTML with cutoff and tooltip"""
        items_truncated_str = ', '.join(my_items[:max_items])
        if not my_items:
            result = None
        elif len(my_items) <= max_items:
            result = items_truncated_str
        else:
            items_truncated_str += ', (...)'
            items_all_str = ', '.join(my_items)
            result = format_html(
                '<span data-tooltip="{}" class="tooltip">{}</span>',
                items_all_str,
                items_truncated_str
            )
        return result

    def _groups(self, obj):
        my_groups = sorted(group.name for group in list(obj.groups.all()))
        return self._list_2_html_w_tooltips(
            my_groups, 250
        )


admin.site.register(UserInGroupFilter, UserInGroupFilterAdmin)


class AltAlliAdmin(admin.ModelAdmin):
    list_select_related = ["alt_alli"]
    list_display = ["__str__", "alt_alli"]
    raw_id_fields = ["alt_alli"]
    filter_horizontal = ["exempt_alliances", "exempt_corporations"]


admin.site.register(AltAllianceFilter, AltAlliAdmin)

admin.site.register(GroupUpdateWebhook)
