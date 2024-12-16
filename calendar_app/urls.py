from django.urls import path
from . import views
from .views import CalendarListView, CalendarWindowDetailView

urlpatterns = [
    path('', views.home, name='home'),
    path('calendar/', 
         CalendarListView.as_view(), 
         name='calendar_list'),
    path('window/<int:pk>/', 
         CalendarWindowDetailView.as_view(), 
         name='window_detail'),
    path('event/edit/<int:event_id>/', 
         views.edit_event, 
         name='edit_event'),
     path('event/create/', views.create_event, name='create_event'),

]
