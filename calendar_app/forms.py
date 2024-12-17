from django import forms
from .models import CalendarWindow, EventAttendance, Rating, Review


class CalendarWindowForm(forms.ModelForm):
    class Meta:
        model = CalendarWindow
        fields = [ 'title', 'content', 'is_event', 'date', 'image', 'video']  # Include title here


class EventEditForm(forms.ModelForm):
    class Meta:
        model = CalendarWindow
        fields = ['title', 'is_event', 'content', 'date', 'image', 'video']  # Include title here


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = EventAttendance
        fields = ['is_attending']


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text']