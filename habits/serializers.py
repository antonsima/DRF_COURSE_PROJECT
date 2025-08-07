from rest_framework.serializers import ModelSerializer

from habits.models import Habit


class HabitSerializer(ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'

    def validate(self, data):
        pass

    def validate_time_to_complete(self):
        pass

    ...