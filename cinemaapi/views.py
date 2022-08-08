from rest_framework.viewsets import ViewSet, ModelViewSet
from cinemaapi.models import Cinema, Reviews
from cinemaapi.serializers import CinemaSerializer, UserSerializer, LogInSerializer, ReviewsSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework.decorators import action


class UserCreationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignInView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LogInSerializer(data=request.data)
        if serializer.is_valid():
            uname = serializer.validated_data.get("username")
            password = serializer.validated_data.get("password")
            user = authenticate(request, username=uname, password=password)
            if user:
                login(request, user)
                return Response({"msg": "Success"})
            else:
                return Response({"msg": "Invalid User"})


class CinemaViewSetView(ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model = Cinema
    serializer_class = CinemaSerializer
    queryset = Cinema.objects.all()

    def get_queryset(self):
        return Cinema.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = CinemaSerializer(data=request.data, context={"user": request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    @action(methods=["post", ], detail=True)
    def add_review(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        movie = Cinema.objects.get(id=id)
        user = request.user
        serializer = ReviewsSerializer(data=request.data, context={"movie": movie, "user": user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)
