from django.apps import AppConfig

class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'

    def ready(self):
        from django.contrib.auth.models import User
        from .models import CartItems

        def get_cart_count(self):
            return CartItems.objects.filter(cart__is_paid=False, cart__user=self).count()

        User.add_to_class("get_cart_count", get_cart_count)
