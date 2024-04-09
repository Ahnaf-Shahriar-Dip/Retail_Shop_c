from django.apps import AppConfig


class Product_Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Product'

    


    def ready(self):
        import Product.views  # Make sure to replace 'your_app_name' with the actual name of your app