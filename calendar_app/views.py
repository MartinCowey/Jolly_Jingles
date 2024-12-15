from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CalendarWindow
from django.utils import timezone

# Home view to display events and information about Code Institute
def home(request):
    events = CalendarWindow.objects.filter(is_event=True)  # Adjust this query as needed
    return render(request, 'calendar_app/home.html', {
        'events': events,
        'current_year': timezone.now().year,
    })


class CalendarListView(LoginRequiredMixin, ListView):
    model = CalendarWindow
    template_name = 'calendar_app/calendar_list.html'
    context_object_name = 'windows'


class CalendarWindowDetailView(LoginRequiredMixin, DetailView):
    model = CalendarWindow
    template_name = 'calendar_app/window_detail.html'
    context_object_name = 'window'
