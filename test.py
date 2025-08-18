from users.models import User

User.objects.filter(id__in=[bad_ids]).delete()