from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from habits.serializers import HabitSerializer


class HabitViewSet(ModelViewSet):
    model = Habit
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = []
    pagination_class = []

