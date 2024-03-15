from django.core.management.base import BaseCommand
from charts.models import ExpenseCategory


class Command(BaseCommand):
    help = "create expense types"
    def handle(self, *args, **options):
        ExpenseCategory.objects.bulk_create(
[           ExpenseCategory(name='Medicin'),
            ExpenseCategory(name='Transport'),
            ExpenseCategory(name='Cloths'),
            ExpenseCategory(name='House & Renovation'),
            ExpenseCategory(name='Food'),
            ExpenseCategory(name='Leisure'),]
        )
        self.stdout.write(self.style.SUCCESS("Successfully created expense types."))

