from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Cinema(models.Model):
    movie_name = models.CharField(max_length=120)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    release_year = models.CharField(max_length=5)
    director_name = models.CharField(max_length=99)
    movie_image = models.ImageField(upload_to="movie_images", null=True)

    def __str__(self):
        return self.movie_name

    def average_rating(self):

        reviews = Reviews.objects.filter(movie=self)
        if len(reviews) > 0:
            total = sum([review.rating for review in reviews])
            return total / len(reviews)
        else:
            return 0


class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.CharField(max_length=200)
    movie = models.ForeignKey(Cinema, on_delete=models.DO_NOTHING)
    rating = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = ("user", "movie")
