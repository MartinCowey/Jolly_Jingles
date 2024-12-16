from django import forms
from .models import CalendarWindow, EventAttendance

class CalendarWindowForm(forms.ModelForm):
    class Meta:
        model = CalendarWindow
        fields = ['number', 'content', 'is_event', 'date', 'image', 'video']  # Include title here

class EventEditForm(forms.ModelForm):
    class Meta:
        model = CalendarWindow
        fields = ['number', 'is_event', 'content', 'image', 'video']  # Include title here

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = EventAttendance
        fields = ['is_attending']
