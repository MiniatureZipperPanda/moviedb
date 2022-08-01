from django.db import models
from django.contrib.auth.models import User


class Cinema(models.Model):
    movie_name = models.CharField(max_length=120)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    release_year = models.CharField(max_length=5)
    director_name = models.CharField(max_length=99)
    movie_image = models.ImageField(upload_to="movie_images",null=True)

    def __str__(self):
        return self.movie_name
