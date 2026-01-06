from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Create a superuser with default credentials'

    def handle(self, *args, **options):
        User = get_user_model()
        
        if not User.objects.filter(email='admin@example.com').exists():
            user = User.objects.create_superuser(
                email='admin@example.com',
                username='admin',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write(
                self.style.SUCCESS('Successfully created superuser: admin@example.com')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Superuser admin@example.com already exists')
            )