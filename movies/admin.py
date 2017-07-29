from django.contrib import admin

from . import models

@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Director)
class DirectorAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Actor)
class ActorAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Movie)
class MovieAdmin(admin.ModelAdmin):
    pass

@admin.register(models.GenreRating)
class GenreRatingAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Rating)
class RatingAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Profile)
class RatingAdmin(admin.ModelAdmin):
    pass