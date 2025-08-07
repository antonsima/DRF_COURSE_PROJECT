from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'habits'

router = DefaultRouter()
router.register('habits', HabitViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('habits/', include('habits.urls', namespace='habits')),
    path('users/', include('users.urls', namespace='users')),
]
