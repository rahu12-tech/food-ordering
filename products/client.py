import razorpay
from django.conf import settings

class Client:
    def __init__(self):
        self.client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

    def payment_request_create(self, amount, purpose, buyer_name, email, redirect_url):
        order_data = {
            'amount': float(amount),  # Convert Decimal to float
            'currency': 'INR',
            'receipt': 'order_rcptid_11',
            'payment_capture': '1',
            'notes': {
                'purpose': purpose,
                'buyer_name': buyer_name,
                'email': email,
                'redirect_url': redirect_url
            }
        }
        return self.client.order.create(order_data)
