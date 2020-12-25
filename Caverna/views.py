from django.contrib.auth import get_user_model
from rest_framework import generics

from .serializers import CreateUserSerializer


class RegisterView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = CreateUserSerializer