from . import views
from django.urls import path
from .views import CalendarListView, CalendarWindowDetailView, home

urlpatterns = [
    path('', home, name='home'),  # This sets the home view as the default landing page
    path('calendar/', CalendarListView.as_view(), name='calendar_list'),
    path('window/<int:pk>/', CalendarWindowDetailView.as_view(), name='window_detail'),
]
