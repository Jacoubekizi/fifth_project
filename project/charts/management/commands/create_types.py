from django.core.management.base import BaseCommand
from charts.models import Expense_Type


class Command(BaseCommand):
    help = "create expense types"
    def handle(self, *args, **options):
        Expense_Type.objects.bulk_create(
[            Expense_Type(expense_name='Medicin'),
            Expense_Type(expense_name='Transport'),
            Expense_Type(expense_name='Cloths'),
            Expense_Type(expense_name='House & Renovation'),
            Expense_Type(expense_name='Food'),
            Expense_Type(expense_name='Leisure'),]
        )
        self.stdout.write(self.style.SUCCESS("Successfully created expense types."))