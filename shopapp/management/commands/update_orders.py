from django.core.management.base import BaseCommand

from shopapp.models import Order, Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        order = Order.objects.first()
        if not order:
            self.stdout.write('Order not found.')
            return

        products = Product.objects.all()

        for p in products:
            order.products.add(p)

        order.save()
        self.stdout.write('Products saved')