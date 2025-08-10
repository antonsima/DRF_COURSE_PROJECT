from rest_framework.serializers import ModelSerializer

from habits.models import Habit
from habits.validators import CreateHabitValidator, UpdateHabitValidator


class HabitSerializer(ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("user",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance:
            self.validators = [UpdateHabitValidator(instance=self.instance)]
        else:
            self.validators = [CreateHabitValidator()]


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
