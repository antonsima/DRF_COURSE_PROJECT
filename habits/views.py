from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from habits.paginators import HabitsPaginator
from habits.serializers import HabitSerializer, PublicHabitSerializer
from users.permissions import IsOwner


class HabitViewSet(ModelViewSet):
    model = Habit
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = HabitsPaginator

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (IsAuthenticated,)
        elif self.action in ["update", "retrieve", "destroy"]:
            self.permission_classes = (IsAuthenticated, IsOwner)
        return super().get_permissions()


class PublicHabitListAPIView(generics.ListAPIView):
    model = Habit
    queryset = Habit.objects.filter(is_public=True)
    serializer_class = PublicHabitSerializer
    pagination_class = HabitsPaginator


class PublicHabitRetrieveAPIView(generics.RetrieveAPIView):
    model = Habit
    serializer_class = PublicHabitSerializer
    queryset = Habit.objects.filter(is_public=True)