from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from shopapp.models import Order


class Command(BaseCommand):
    ''' Create orders '''
    def handle(self, *args, **options):
        self.stdout.write('Creating orders...')
        user = User.objects.get(username='admin')
        lst = [
            {'address': 'Mira', 'promo': '123asd'},
            {'address': 'Lenina', 'promo': ''},
            {'address': 'Proletarskaya', 'promo': ''},
            {'address': 'Kosmonavtov', 'promo': '321ewq'},
        ]
        for i in lst:
            item, res = Order.objects.get_or_create(delivery_address=i['address'], promo_code=i['promo'], user=user)
            self.stdout.write(f'Created order: {item}')
        self.stdout.write(self.style.SUCCESS('Orders Created'))