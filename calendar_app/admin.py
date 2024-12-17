from django.contrib import admin
from .models import CalendarWindow

@admin.register(CalendarWindow)
class CalendarWindowAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'content', 'is_event', 'date')  # Customize fields to display
    search_fields = ('title', 'content')  # Add search functionality if needed
