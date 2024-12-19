from django.core.management.base import BaseCommand
from ...views import add_recommendations

class Command(BaseCommand):
    help = 'Adds energy-saving recommendations to the database'

    def handle(self, *args, **kwargs):
        add_recommendations()
        self.stdout.write(self.style.SUCCESS('Successfully added energy-saving recommendations.'))

# # run this command to populate DB
# python manage.py add_recommendations    