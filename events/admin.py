from django.contrib import admin
from .models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'organiser')
    list_filter = ('date', 'location', 'organiser')
    search_fields = ('title', 'date', 'location', 'organiser__username', 'description')
    ordering = ('-date',)
    date_hierarchy = 'date'
    readonly_fields = ('organiser',)
    filter_horizontal = ('attendees', )

    def get_queryset(self, request):
        qs = admin.ModelAdmin.get_queryset(self, request)
        if not request.user.is_superuser:
            qs = qs.filter(organiser=request.user)
        return qs

    def save_model(self, request, obj, form, change):
        if not change or not obj.organiser:
            obj.organiser = request.user
        obj.save()


admin.site.register(Event, EventAdmin)
