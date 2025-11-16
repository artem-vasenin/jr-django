from ..views import CartView, CheckoutView

urls = [
    # Заказы
    ("orders:cart", CartView, "???", 200),
    ("orders:checkout", CheckoutView, "???", 200),
]