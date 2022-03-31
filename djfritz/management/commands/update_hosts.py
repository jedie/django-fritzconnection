from django.core.management.base import BaseCommand

from djfritz.services.hosts import update_hosts


class Command(BaseCommand):
    help = 'Update the Host model from current FritzBox Connection'

    def handle(self, *args, **options):
        message = update_hosts()
        print(message)
