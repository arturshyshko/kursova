from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Movie, Profile, User, Genre, Rating
from .forms import LoginForm, LogoutForm, RegisterForm, SearchForm
from .forms import AddFilmToUserListForm, get_rate_film_form

AMOUNT = 20

class Table:
    def __init__(self, ratings, movies, genres):
        _ratings = list(ratings)
        movie_pks = set()
        genre_pks = set()
        self.movies = []
        self.genres = []
        for rating in _ratings:
            movie = rating.movie
            genre = rating.genre
            if movie.pk not in movie_pks:
                self.movies.append(movie)
                movie_pks.add(movie.pk)
            if genre.pk not in genre_pks:
                self.genres.append(genre)
                genre_pks.add(genre.pk)
        for movie in list(movies):
            if movie.pk not in movie_pks:
                self.movies.append(movie)
                movie_pks.add(movie.pk)
        for genre in list(genres):
            if genre.pk not in genre_pks:
                self.genres.append(genre)
                genre_pks.add(genre.pk)
        self.table = {
            m.name: {
              g.name: (
                [x.position
                 for x in _ratings
                 if x.movie.pk == m.pk and x.genre.pk == g.pk][0]
                if len(list(
                 x.position
                 for x in _ratings
                 if x.movie.pk == m.pk and x.genre.pk == g.pk))  > 0
                else None
              )
              for g in self.genres
            }
            for m in self.movies
        }

def index(request):
    return render(request, 'movies/base.html',)


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            profile = auth.authenticate(
                username = form.cleaned_data['login'],
                password = form.cleaned_data['password']
            )
            if profile is not None:
                auth.login(request, profile)
            return render(request, 'movies/base.html', {
                'user': Profile.objects.get(username = profile.username)
            })
    else:
        form = LoginForm()
    return render(request, 'movies/login.html', {'form': form})


def logout(request):
    if request.method == 'POST':
        form = LogoutForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                auth.logout(request)
            return render(request, 'movies/base.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            newuser = Profile.objects.create_user(
                form.cleaned_data['username'],
                form.cleaned_data['email'],
                )
            if form.cleaned_data['first_name']:
                newuser.first_name = form.cleaned_data['first_name']
            if form.cleaned_data['last_name']:
                newuser.last_name = form.cleaned_data['last_name']
            newuser.is_staff = False
            return render(request, 'movies/base.html')
    else:
        form = RegisterForm()
    return render(request, 'movies/register.html', {'form': form})


def cabinet(request, name):
    user = Profile.objects.get(username=name)
    return render(request, 'movies/cabinet.html', {'user': user})


def userList(request, name):
    ratings = (
        Rating.objects
        .filter(profile=request.user)
        .order_by('movie__name')
    )
    table = Table(ratings, request.user.movies.all(), Genre.objects.all())
    return render(request, 'movies/userFilmList.html', {
        'table': table,
    })


def listByGenre(request, name, genre):
    user = Profile.objects.get(username = name)
    _genre = Genre.objects.get(name = genre)
    return render(request, 'movies/userGenreRating.html', {
        'genre': _genre,
        'user': user,
    })


def movieList(request):
    genres = Genre.objects.all()
    form = SearchForm()

    if request.method == 'GET':
        movieName = request.GET.get('movie_name')
        movies_list = Movie.objects.all()
        for genre in genres:
            if request.GET.get(genre.name) and movieName:
                movies_list = movies_list.filter(genres__genre=genre)
                movies_list = movies_list.filter(name__contains=movieName)
            elif request.GET.get(genre.name):
                movies_list = movies_list.filter(genres__genre=genre)
            elif movieName:
                movies_list = movies_list.filter(name__contains=movieName)
        paginator = Paginator(movies_list, AMOUNT)
        page = request.GET.get('page')
        try:
            movies = paginator.page(page)
        except PageNotAnInteger:
            movies = paginator.page(1)
        except EmptyPage:
            paginator.page(paginator.num_pages)
            movies = paginator.page(paginator.num_pages)
        return render(request, 'movies/movies.html', {
            'movies': movies,
            'genres': genres,
            'form': form,
            })

    film_list = Movie.objects.all()
    paginator = Paginator(film_list, AMOUNT)
    page = request.GET.get('page')
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        paginator.page(paginator.num_pages)
        movies = paginator.page(paginator.num_pages)
    return render(request, 'movies/movies.html', {
        'movies': Movie.objects.all(),
        'form': form,
        'genres': genres,
    })


def movie(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    user = request.user
    form = get_rate_film_form(Movie.objects.get(pk=movie_pk))()
    return render(request, 'movies/movie.html', {
        'movie': movie,
        'user': user,
        'form': form
    })


def add(request, movie_pk):
    if request.method == 'POST':
        form = AddFilmToUserListForm(request.POST)
        if form.is_valid():
            prof = request.user
            movie = Movie.objects.get(pk=movie_pk)
            movie.users.add(prof)
            return render(request, 'movies/movie.html', {'movie': movie})


def rate(request, movie_pk, name):
    if request.method == 'POST':
        movie = Movie.objects.get(pk=movie_pk)
        form = get_rate_film_form(movie)(request.POST)
        if form.is_valid():
            rate = request.user.rate(movie, form.cleaned_data['genre'],
                form.cleaned_data['position'])
            # position = form.cleaned_data['position']
            # if position > request.user.movies.count():
            #     position = request.user.movies.count()
            # rate, created = Rating.objects.get(
            #     profile = request.user,
            #     genre = form.cleaned_data['genre'],
            #     movie = movie
            #     position=position
            # )
            # form.set_position(rate.position)
            form.cleaned_data['position'] = rate.position
            return render(request, 'movies/movie.html', {
                'movie': movie,
                'form': form,
            })