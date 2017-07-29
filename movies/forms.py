from django import forms
from django.core.validators import MinValueValidator

from .models import Genre, GenreRating

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150, label='Login')
    first_name = forms.CharField(max_length=150, label='First Name', required=False)
    last_name = forms.CharField(max_length=150, label='Second Name', required=False)
    email = forms.EmailField(label='Email', required=False)
    password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput,
        label='Password'
    )
    check_password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput,
        label='Repeat password')


class LoginForm(forms.Form):
    login = forms.CharField(max_length=100, label='Login (nickname)')
    password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput,
        label='Password'
    )


class LogoutForm(forms.Form):
    logout = forms.BooleanField(label='logout', required=True)


class AddFilmToUserListForm(forms.Form):
    pass


def get_rate_film_form(movie):
    q = Genre.objects.filter(
        pk__in=GenreRating.objects.filter(movie=movie).values_list('pk', flat=True)
    )

    class RateFilmForm(forms.Form):
        genre = forms.ModelChoiceField(queryset=q)
        position = forms.IntegerField(validators=[MinValueValidator(1)])

    return RateFilmForm


class SearchForm(forms.Form):
    movie_name = forms.CharField(
        max_length=150,
        required=False,
        widget = forms.TextInput(attrs = {'placeholder': 'Search for films'}),
        )