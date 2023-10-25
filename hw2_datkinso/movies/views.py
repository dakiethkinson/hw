from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView

from .forms import BookingForm
from .models import Movie, Booking
from django.views import View

class MovieListView(View):
    def get(self, request):
        movies = Movie.objects.all()
        return render(request, 'movies/movie_list.html', {'movies': movies})

class BookMovieView(View):
    template_name = 'booking.html'

    def get(self, request, *args, **kwargs):
        movie_id = kwargs['movie_id']
        movie = get_object_or_404(Movie, id=movie_id)
        context = {
            'movie': movie
        }
        return render(request, self.template_name, context)

    def get(self, request, movie_id):
        form = BookingForm(initial={'movie': movie_id})
        return render(request, 'movies/booking.html', {'form': form})

    def post(self, request, movie_id):
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movie-list')
        return render(request, 'movies/booking.html', {'form': form})

class BookedMoviesView(View):
    template_name = 'booked_movies.html'

    def get(self, request, *args, **kwargs):
        bookings = Booking.objects.all()
        context = {
            'bookings': bookings
        }
        return render(request, self.template_name, context)
