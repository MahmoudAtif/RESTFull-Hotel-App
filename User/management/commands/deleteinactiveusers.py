from django.core.management.base import BaseCommand
from User.models import User
from django.utils import timezone


class Command(BaseCommand):
    """ Django command to delete inactivated users """

    def handle(self, *args, **options):
        users = User.objects.filter(
            date_joined__lt=timezone.now() - timezone.timedelta(days=2),
            is_active=False
        )
        if len(users) > 0:
            users.delete()
            return 'Deleted Successfully'

        return 'not exist users outdate'
