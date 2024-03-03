import random
from datetime import datetime, timedelta
import pytz
from django.core.management.base import BaseCommand
from charts.models import Item , Expense_Type


class Command(BaseCommand):
    help = "populate DB with Data"
    def add_arguments(self,parser):
        parser.add_argument("--amount", type=int, help="The number of items that should be created.")
    def handle(self, *args, **options):
        types = list(Expense_Type.objects.all())

        amount = options["amount"] if options["amount"] else 500

        for i in range(0,amount):
            dt = pytz.utc.localize(datetime.now() - timedelta(days = random.randint(0 , 1825)))
            expense = Item.objects.create(
                item_name = str(f'item {i}'),
                price = random.randrange(500,50000,50),
                expense_type = random.choice(types)
            )
            expense.time_purchased = dt
            expense.save()

        self.stdout.write(self.style.SUCCESS("Successfully populated the database."))

