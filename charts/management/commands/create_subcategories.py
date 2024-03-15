from django.core.management.base import BaseCommand
from charts.models import ExpenseSubCategory , ExpenseCategory


class Command(BaseCommand):
    help = "create expense types"
    def handle(self, *args, **options):
        ExpenseSubCategory.objects.bulk_create(
[           ExpenseSubCategory(name='Doctor'),
            ExpenseSubCategory(name='Transport'),
            ExpenseSubCategory(name='Cloths'),
            ExpenseSubCategory(name='House & Renovation'),
            ExpenseSubCategory(name='Food'),
            ExpenseSubCategory(name='Leisure'),]
        )
        self.stdout.write(self.style.SUCCESS("Successfully created expense types."))

