from django.test import TestCase
from utils import *

# Create your tests here.
request.COOKIES: {'csrftoken': 'LHE9WlKGNiy7DzMjQR86Sxjlwv3N7y97hb1tPm8GwBckzuMVo6wuYdynGoQy67Xz', 'cart': '{"2":{"quantity":1}}'}
data: {'form': {'name': 'l', 'email': 'l', 'total': '14.99'}, 'shipping': {'address': 'l', 'city': 'l', 'state': 'l', 'zipcode': 'l', 'country': 'w'}}

print(guestOrder(request.COOKIES,data))