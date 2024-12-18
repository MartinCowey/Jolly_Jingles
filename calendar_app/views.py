from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CalendarWindow, EventAttendance, Rating, Review
from .forms import EventEditForm, AttendanceForm, CalendarWindowForm, RatingForm, ReviewForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required



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


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventEditForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.date = request.POST.get('date')
            event.is_event = True  # Make sure this is set when creating the event
            event.save()
            return redirect('home')

    else:
        form = EventEditForm()  # Render an empty form
        # Dynamically exclude 'title' and 'date' fields
        form.fields.pop('title')
        form.fields.pop('date')

    return render(request, 'calendar_app/create_event.html', {'form': form})
    

def edit_event(request, event_id):
    # Get the CalendarWindow object
    event = get_object_or_404(CalendarWindow, number=event_id)

    # Check if the logged-in user has permission to edit the event
    # Update this logic based on your model fields if necessary
    if not request.user.is_authenticated:
        return redirect('home')  # Redirect unauthorized users

    # Process the form submission
    if request.method == 'POST':
        event_form = EventEditForm(request.POST, request.FILES, instance=event)
        attendance_form = AttendanceForm(request.POST)

        if event_form.is_valid() and attendance_form.is_valid():
                event_form.save()
                attendance_instance = attendance_form.save(commit=False)
                attendance_instance.user = request.user
                attendance_instance.window = event
                attendance_instance.save()

                event.is_event = True  # Make sure this remains True after editing
                event.save()  # Save again in case it's not saved correctly
                print(f"Event ID: {event.number}, is_event: {event.is_event}")  # Debugging line

                return redirect('window_detail', window_number=event.number)
    
    else:
        # Prepopulate the forms for GET requests
        event_form = EventEditForm(instance=event)
        attendance_form = AttendanceForm()

    return render(request, 'calendar_app/edit_event.html', {
        'event': event,
        'event_form': event_form,
        'attendance_form': attendance_form,
    })



def delete_event(request, event_id):
    event = get_object_or_404(CalendarWindow, number=event_id)
    if request.method == 'POST':
        event.delete()  # Delete the event from the database
        return redirect('home')  # Redirect to home or another page after deletion
    return render(request, 'calendar_app/delete_event.html', {'event': event})


def your_view(request, window_number):
    window = get_object_or_404(CalendarWindow, number=window_number)
    
    if request.method == 'POST':
        rating_form = RatingForm(request.POST)
        review_form = ReviewForm(request.POST)

        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.window = window
            # Assign the user if logged in, otherwise allow it to be null
            if request.user.is_authenticated:
                rating.user = request.user
            rating.save()

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.window = window
            # Assign the user if logged in, otherwise allow it to be null
            if request.user.is_authenticated:
                review.user = request.user
            review.save()

        # Redirect after saving
        return redirect('window_detail', window_number=window.number)

    else:
        rating_form = RatingForm()
        review_form = ReviewForm()

    context = {
        'window': window,
        'rating_form': rating_form,
        'review_form': review_form,
    }
    
    return render(request, 'calendar_app/window_detail.html', context)




