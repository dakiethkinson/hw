from django.urls import path
from . import views
from .views import BookMovieView, BookedMoviesView

urlpatterns = [
    path('', views.MovieListView.as_view(), name='movie-list'),
    path('movies/<int:movie_id>/book/', BookMovieView.as_view(), name='book-movie'),
    path('booked-movies/', BookedMoviesView.as_view(), name='booked-movies'),
]