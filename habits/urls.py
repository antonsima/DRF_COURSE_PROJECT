from django.urls import path
from rest_framework.routers import DefaultRouter

from habits.views import (
    HabitViewSet,
    PublicHabitListAPIView,
    PublicHabitRetrieveAPIView,
)

app_name = "habits"

router = DefaultRouter()
router.register("", HabitViewSet)


urlpatterns = [
    path(
        "public/<int:pk>/",
        PublicHabitRetrieveAPIView.as_view(),
        name="habit-get",
    ),
    path("public/", PublicHabitListAPIView.as_view(), name="habits-list"),
] + router.urls
