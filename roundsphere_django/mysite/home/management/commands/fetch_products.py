import requests
from django.core.management.base import BaseCommand
from home.models import Product

class Command(BaseCommand):
    help = 'Fetch product data from the external API and populate the database'

    def handle(self, *args, **kwargs):
        # API URL for fetching product data
        url = 'http://127.0.0.1:5000/api/get-all-products'
        
        # Fetch data from the external API
        response = requests.get(url)
        
        # Check if the response is successful
        if response.status_code == 200:
            # Parse the response JSON data
            products_data = response.json()

            # Loop through each product in the fetched data
            for product in products_data:
                # Use update_or_create to either update existing products or create new ones
                Product.objects.update_or_create(
                    productId=product['productId'],  # Assuming productId is the unique identifier
                    defaults={
                        'name': product['name'],
                        'description': product['description'],
                        'price': product['price'],
                        'stock': product['stock'],
                        # If you have an image URL, you can download it and save it to the Product model
                        # If not, you can handle it as required
                        'image': product.get('image', None),  # If image is available in the API response
                    }
                )
            
            self.stdout.write(self.style.SUCCESS('Successfully populated the products data'))
        else:
            self.stdout.write(self.style.ERROR('Failed to fetch data from the API'))
