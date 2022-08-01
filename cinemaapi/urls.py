from django.urls import path
from cinemaapi import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("cinema-model-view-set", views.CinemaViewSetView, basename="cinema-model-view-set"),
urlpatterns = [
                  path('users/account/sign-up', views.UserCreationView.as_view()),
                  path('users/account/sign-in', views.SignInView.as_view()),
              ] + router.urls
