from django.core.management.base import BaseCommand

from shopapp.models import Product


class Command(BaseCommand):
    ''' Create products '''
    def handle(self, *args, **options):
        self.stdout.write('Creating products...')
        lst = [
            {'name': 'Smartphone', 'price': 100},
            {'name': 'Laptop', 'price': 300},
            {'name': 'PocketBook', 'price': 110},
            {'name': 'PC', 'price': 400},
        ]
        for i in lst:
            item, res = Product.objects.get_or_create(name=i['name'], price=i['price'])
            self.stdout.write(f'Created product: {item.name}')
        self.stdout.write(self.style.SUCCESS('Products Created'))