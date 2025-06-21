from django.contrib.admin import register, ModelAdmin, TabularInline
from django.utils.html import format_html
from django.contrib.admin import SimpleListFilter


class BaseEntityAdmin(ModelAdmin):
    list_per_page = 10
    list_display = ['id', 'api']

    def api(self, obj):
        try:
            url = self.api_view.get_url(obj.id)
            return format_html('<a target="_blank" href="%s">View</a>' % url)
        except:
            return

    api.allow_tags = True


class BaseLogInline(TabularInline):
    pass


class BaseEntityActiveAdmin(BaseEntityAdmin):
    list_filter = ['active']


class CustomAdminFilter(SimpleListFilter):
    title = 'custom'
    parameter_name = 'custom'

    lookups_parms = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    def lookups(self, request, model_admin):
        return self.get_lookup_parms()

    def get_lookup_parms(self):
        return self.lookups_parms

    def queryset(self, request, queryset):
        return queryset.all()
