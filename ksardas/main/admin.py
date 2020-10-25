from django.contrib import admin
from .models import AdvUser, CharBase, CharClasses, Spell


class SpellAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'school',
        'level',
    )
    search_fields = (
        'name',
    )

    def get_search_results(self, request, queryset, search_name):
        queryset, use_distinct = super().get_search_results(request, queryset, search_name)
        try:
            search_name_for_sqlite = search_name.upper()
        except ValueError:
            pass
        else:
            queryset |= self.model.objects.filter(name__icontains=search_name_for_sqlite)
        return queryset, use_distinct


class CharClassesAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'caption',
        'description',
    )


admin.site.register(AdvUser)
admin.site.register(CharBase)
admin.site.register(CharClasses, CharClassesAdmin)
admin.site.register(Spell, SpellAdmin)

