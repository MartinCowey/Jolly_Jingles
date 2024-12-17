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


def create_event(request):
    if request.method == 'POST':
        form = EventEditForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)  # Don't commit yet
            event.date = request.POST.get('date')  # Get the date from POST data
            event.save()  # Now save the instance with all fields included
            return redirect('home')  # Redirect after successful creation
    else:
        form = EventEditForm()  # Render an empty form
        # Dynamically exclude 'title' and 'date' fields
        form.fields.pop('title')
        form.fields.pop('date')

    return render(request, 'calendar_app/create_event.html', {'form': form})

def edit_event(request, event_id):
    event = get_object_or_404(CalendarWindow, number=event_id)
    if request.method == 'POST':
        event_form = EventEditForm(request.POST, request.FILES, instance=event)
        attendance_form = AttendanceForm(request.POST)
        if event_form.is_valid() and attendance_form.is_valid():
            # Save the event
            updated_event = event_form.save(commit=False)
            updated_event.is_event = True  # Explicitly set this field
            updated_event.save()

            # Save attendance
            attendance = attendance_form.save(commit=False)
            attendance.user = request.user  # Assuming the user is logged in
            attendance.window = event
            attendance.save()

            return redirect('home')  # Redirect to home after saving changes
    else:
        event_form = EventEditForm(instance=event)
        # Exclude fields dynamically
        event_form.fields.pop('title')
        event_form.fields.pop('date')

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


def delete_event(request, event_id):
    event = get_object_or_404(CalendarWindow, number=event_id)
    if request.method == 'POST':
        event.delete()  # Delete the event from the database
        return redirect('home')  # Redirect to home or another page after deletion
    return render(request, 'calendar_app/delete_event.html', {'event': event})


def your_view(request, window_number):
    window = get_object_or_404(CalendarWindow, number=window_number)
    form = CalendarWindowForm(instance=window)
    return render(request, 'calendar_app/window_detail.html', {'window': window, 'form': form})
