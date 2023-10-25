from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    showtimes = models.DateTimeField()

    def __str__(self):
        return self.title

class Booking(models.Model):
    user = models.CharField(max_length=100)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    seat_number = models.IntegerField()
