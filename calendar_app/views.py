from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CalendarWindow, EventAttendance
from .forms import EventEditForm, AttendanceForm, CalendarWindowForm
from django.utils import timezone

# Home view to display events and information about Code Institute
def home(request):
    events = CalendarWindow.objects.filter(is_event=True)[:6]  # Adjust
    print("Number of events fetched:", events.count())
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

def edit_event(request, event_id):
    event = get_object_or_404(CalendarWindow, number=event_id)
    if request.method == 'POST':
        event_form = EventEditForm(request.POST, request.FILES, instance=event)
        attendance_form = AttendanceForm(request.POST)
        if event_form.is_valid() and attendance_form.is_valid():
            event_form.save()
            attendance = attendance_form.save(commit=False)
            attendance.user = request.user  # Assuming the user is logged in
            attendance.window = event
            attendance.save()
            return redirect('window_detail', pk=event.id)
    else:
        event_form = EventEditForm(instance=event)
        attendance_instance = EventAttendance.objects.filter(
            user=request.user, window=event
        ).first()
        attendance_form = (
            AttendanceForm(instance=attendance_instance)
            if attendance_instance
            else AttendanceForm()
        )

    context = {
        'event_form': event_form,
        'attendance_form': attendance_form,
        'event': event,
    }
    return render(request, 'calendar_app/edit_event.html', context)

def create_event(request):
    if request.method == 'POST':
        form = EventEditForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)  # Save the form but don't commit yet
            # Get the date from the POST data
            event.date = request.POST.get('date')  # Ensure you have a 'date' field in your model
            event.save()  # Now save the instance with the date included
            return redirect('home')  # Redirect after successful creation
        else:
            # If the form is invalid, re-render the form with errors
            return render(request, 'calendar_app/create_event.html', {'form': form})
    else:
        # If it's a GET request, render an empty form
        form = EventEditForm()
    
    return render(request, 'calendar_app/create_event.html', {'form': form})

def your_view(request, window_number):
    window = get_object_or_404(CalendarWindow, number=window_number)
    form = CalendarWindowForm(instance=window)
    return render(request, 'calendar_app/window_detail.html', {'window': window, 'form': form})
