from django.urls import path
from . import views
from .views import CalendarListView

urlpatterns = [
    path('', views.home, name='home'),
    path('calendar/', CalendarListView.as_view(), name='calendar_list'),
    path('window/<int:window_number>/', views.your_view, name='window_detail'),
    path('event/create/', views.create_event, name='create_event'),
    path('event/edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('event/delete/<int:event_id>/', views.delete_event, name='delete_event'),
]
