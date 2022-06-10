from ctypes import addressof
import email
from operator import truediv
from ssl import create_default_context
from types import CoroutineType
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from coupon.models import Coupon

# Create your models here.
class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    coupon = models.ForeignKey(Coupon, on_delete=models.PROTECT, related_name='order_coupon', null=True, blank=True)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100000)])

    class Meta:
        ordering = ['-created']
    
    # __str__ 메소드 : 관리자 페이지 or delete 페이지에서 객체 정보를 009화면에 출력했을때 어떤 내용을 보여줄지 정하는 메소드
    #                  Django 문법이 아니고 python 기본 문법
    def __str__(self):
        return f'Order {self.id}'
    

    def get_total_product(self):
        return sum(item.get_item_price() for item in self.items.all())


    def get_total_price(self):
        total_product = self.get_total_product()
        return total_product - self.discount
