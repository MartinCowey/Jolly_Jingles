from django import forms
from .models import CalendarWindow, EventAttendance

class CalendarWindowForm(forms.ModelForm):
    class Meta:
        model = CalendarWindow
        fields = ['number', 'content', 'is_event', 'date', 'image', 'video']  # Include all fields

class EventEditForm(forms.ModelForm):
    class Meta:
        model = CalendarWindow
        fields = ['content', 'image', 'video']  # Exclude 'date' from here

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = EventAttendance
        fields = ['is_attending']
