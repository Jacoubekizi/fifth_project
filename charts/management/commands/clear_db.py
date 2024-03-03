from django.core.management.base import BaseCommand
from charts.models import Item


class Command(BaseCommand):
    help = "Clear the DB"
    def handle(self, *args, **options):
        Item.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Successfully cleared the database."))

