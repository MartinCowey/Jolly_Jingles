from django.db import models
from django.contrib.auth.models import User


class CalendarWindow(models.Model):
    number = models.IntegerField(
        primary_key=True,
        choices=[(i, i) for i in range(1, 25)]
    )
    title = models.CharField(max_length=255, default='Untitled')  # Set a default value
    content = models.TextField()
    is_event = models.BooleanField()
    date = models.DateTimeField(null=True)
    image = models.ImageField(
        upload_to='calendar_images/',
        null=True,
        blank=True
    )
    video = models.FileField(
        upload_to='calendar_videos/',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    window = models.ForeignKey(CalendarWindow, on_delete=models.CASCADE)
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    date_rated = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    window = models.ForeignKey(CalendarWindow, on_delete=models.CASCADE)
    text = models.TextField()
    date_reviewed = models.DateTimeField(auto_now_add=True)


class EventAttendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    window = models.ForeignKey(CalendarWindow, on_delete=models.CASCADE)
    is_attending = models.BooleanField(default=False)
