from django.core.management.base import BaseCommand
import sys
import os

# Add the root directory to path so it can import main, authentification, etc.
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from main import main

class Command(BaseCommand):
    help = 'Runs the E-learning CLI application'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting E-learning CLI...'))
        try:
            main()
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('\nCLI interrupted by user.'))
