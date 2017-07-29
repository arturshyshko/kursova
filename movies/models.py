from django.db import models, transaction
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.db.models import F, Q
from django.contrib.auth.models import AbstractUser
import os

class Genre(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=150, blank=False, null=False)

    def __str__(self):
        return self.name


class Movie(models.Model):
    name = models.CharField(max_length=150, blank=False, null=False)
    year = models.IntegerField(validators=[MinValueValidator(1800)])
    country = models.ManyToManyField(
        'Country',
        related_name='movies',
        related_query_name='movie'
    )
    description = models.TextField(blank=False, null=False)
    director = models.ForeignKey('Director', related_name='movies')
    image = models.ImageField(upload_to="images/")
    actors = models.ManyToManyField(
        'Actor',
        related_name='movies',
        related_query_name='movie'
    )
    users = models.ManyToManyField(
        'Profile',
        related_name='movies',
        related_query_name='movie',
    )

    @property
    def the_name(self):
        if not self.name.lower().startswith('the '):
            return self.name
        return self.name[4:] + ', The'

    @property
    def get_genres(self):
        query = self.genres.all()
        names = []
        for q in query:
            names.append(q.genre.name)
        return name

    def __str__(self):
        return '{}, {}'.format(self.the_name, self.year)


class GenreRating(models.Model):
    movie = models.ForeignKey('Movie', related_name='genres')
    genre = models.ForeignKey('Genre', related_name='movie_ratings')
    position = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ('movie', 'position',)

    def __str__(self):
        return '{}, {}, {}'.format(self.position, self.genre, self.movie)


class Rating(models.Model):
    profile = models.ForeignKey('Profile', related_name='ratings')
    genre = models.ForeignKey('Genre', related_name='ratings')
    movie = models.ForeignKey('Movie', related_name='ratings')
    position = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return '{} {} {} {}'.format(
            self.profile.username,
            self.genre.name,
            self.movie.name,
            self.position
        )


class GlobalRating(models.Model):
    movie = models.ForeignKey('Movie', related_name='globalRate')
    position = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ('movie', 'position',)

    def update(): #need formula for rating
        # GlobalRating.objects.all().delete()
        # points = {}
        # for movie in Movie.objects.all():
        #     for user in Profile.objects.all():
        #         if movie in user.movies.all():
        #             for genre in movie.genres:
        #                 try:
        #                     rate = Rating.objects.filter(
        #                         profile = user,
        #                         movie = movie,
        #                         genre = genre
        #                         )
        #                     points[]
        pass


class Profile(AbstractUser):
    def rate(self, movie, genre, position):
        if genre.pk not in movie.genres.values_list('pk', flat=True):
            raise ValueError('Movie {} is not of genre {}'.format(
                movie,
                genre
            ))
        ratings = self.ratings.filter(genre=genre)
        if position > ratings.count() + 1:
            position = ratings.count()+1
        try:
            old_position = (Rating.objects
                .get(profile = self, genre =genre, movie = movie)
                .position)
        except:
            old_position = None
        with transaction.atomic():
            (
                movie.ratings
                .filter(position__gte=position)
                .update(position=F('position')+1)
            )
            if old_position:
                (
                    ratings
                    .filter(position__lte=position)
                    .filter(position__gt=old_position)
                    .update(position=F('position')-1)
                )
            rate, created = Rating.objects.update_or_create(
                profile=self,
                genre=genre,
                movie=movie,
                position=position
            )
            return rate