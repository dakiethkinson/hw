from unittest import TestCase

from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from .models import Movie, Booking
from datetime import datetime, timedelta

from .serializers import MovieSerializer


class MovieIntegrationTests(APITestCase):
    def setUp(self):
        # Setting a future showtime for simplicity in the required format
        future_showtime = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S%z')
        # Create a test movie
        self.movie = Movie.objects.create(title="Test Movie", description="Test Description", showtimes=future_showtime)
        self.booking = Booking.objects.create(user="testuser", movie=self.movie, seat_number=1)


    def test_movie_listings(self):
        response = self.client.get(reverse("movie-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_movie_booking_happy_path(self):
        response = self.client.post(f'/movies/movies/{self.movie.id}/book/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_booked_movies(self):
        response = self.client.get(reverse('booked-movies'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class MovieCreationTest(TestCase):

    def test_create_movie(self):
        movie = Movie.objects.create(
            title="Test Movie",
            description="A movie for testing purposes",
            showtimes="2023-11-01 14:00:00"
        )
        self.assertTrue(isinstance(movie, Movie))
        self.assertEqual(movie.title, "Test Movie")

class BookingCreationTest(TestCase):

    def setUp(self):
        self.movie = Movie.objects.create(
            title="Another Test Movie",
            description="A different movie for testing purposes",
            showtimes="2023-11-02 16:00:00"
        )

    def test_create_booking(self):
        booking = Booking.objects.create(
            user="testuser",
            movie=self.movie,
            seat_number=1
        )
        self.assertTrue(isinstance(booking, Booking))
        self.assertEqual(booking.movie.title, "Another Test Movie")

class MovieSerializerTest(TestCase):

    def setUp(self):
        self.movie_attributes = {
            'title': 'Test Movie',
            'description': 'Description for test movie',
            'showtimes': "2023-10-25 12:00:00"
            # Add other fields as needed
        }
        self.movie = Movie.objects.create(**self.movie_attributes)
        self.serializer = MovieSerializer(instance=self.movie)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'title', 'description', 'showtimes']))

    def test_title_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['title'], self.movie_attributes['title'])