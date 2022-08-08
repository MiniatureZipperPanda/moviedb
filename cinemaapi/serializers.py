from rest_framework.serializers import ModelSerializer
from cinemaapi.models import Cinema, Reviews
from django.contrib.auth.models import User
from rest_framework import serializers


class CinemaSerializer(ModelSerializer):
    user = serializers.CharField(read_only=True)
    id = serializers.CharField(read_only=True)

    class Meta:
        model = Cinema
        fields = ["id", "movie_name", "user", "release_year", "director_name", "movie_image"]

    def create(self, validated_data):
        user = self.context.get("user")
        return Cinema.objects.create(**validated_data, user=user)


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ReviewsSerializer(ModelSerializer):
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Reviews
        exclude = ["movie"]

    def create(self, validated_data):
        user = self.context.get("user")
        movie = self.context.get("movie")
        return Reviews.objects.create(user=user, movie=movie, **validated_data)


class LogInSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
