from decimal import Decimal
from django.conf import settings
from requests import request

from shop.models import Product

class Cart(object):
    def __init__(self):     #초기화 작업
        self.session = request.session
        cart = self.session.get(settings.CART_ID)
        if not cart:
            cart = self.session[settings.CART_ID] = {}
        self.cart = cart
        

    def __len__(self):      #list, dictionary에 사용되는 메서드
        return sum(item['quantity'] for item in self.cart.values())
        # cart에 제품들이 담겨있을거고 그 제품 안에 quantity라는 항목이 있을건데 그걸 전부 더해주는 구문

    def __iter__(self):     #for문 사용할때 어떤식으로 건내줄건지
        product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']

            yield item

    def add(self, product, quantity=1, is_update=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity':0, 'price':str(product.price)}

        if is_update:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        
        self.save()

    def save(self):
        self.session[settings.CART_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del(self.cart[product_id])
            self.save()

    def clear(self):
        self.session[settings.CART_ID] = {}
        self.session.modified = True

    def get_product_total(self):
        return sum(item['price']*item['quantity'] for item in self.cart.values())

