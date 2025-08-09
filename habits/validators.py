from rest_framework.exceptions import ValidationError

from habits.models import Habit


class HabitValidator:
    def __call__(self, attrs):
        self.validate_pleasant_habit(attrs)
        self.validate_useful_habit(attrs)

    def validate_pleasant_habit(self, attrs):
        if attrs.get('is_pleasant'):
            reward = attrs.get('reward')
            linked_habit = attrs.get('linked_habit')

            if reward:
                raise ValidationError(
                    "У приятной привычки не может быть вознаграждения"
                )
            if linked_habit:
                raise ValidationError(
                    "У приятной привычки не может быть связанной привычки"
                )

    def validate_useful_habit(self, attrs):
        is_pleasant = attrs.get('is_pleasant')

        if not is_pleasant:
            reward = attrs.get('reward')
            linked_habit = attrs.get('linked_habit')

            if not reward and not linked_habit:
                raise ValidationError(
                    "У полезной привычки должно быть либо вознаграждение, либо связанная привычка"
                )
            elif reward and linked_habit:
                raise ValidationError(
                    "У полезной привычки должно быть либо вознаграждение, либо связанная привычка"
                )
            if linked_habit:
                linked_habit = Habit.objects.get(id=attrs["linked_habit"].id)
                if not linked_habit.is_pleasant:
                    raise ValidationError("Связанная привычка должна быть приятной")
