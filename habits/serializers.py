from rest_framework.serializers import ModelSerializer
from habits.models import Habit
from habits.validators import HabitValidator


class HabitSerializer(ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('user',)
        validators = [HabitValidator()]


class PublicHabitSerializer(ModelSerializer):
    class Meta:
        model = Habit
        fields = [
            "time",
            "action",
            "is_pleasant",
            "periodicity",
            "time_to_complete",
            "user__first_name_",
        ]
