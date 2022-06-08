from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
# POST로만 접근할 수 있도록 해주는 구문

# Create your views here.

from shop.models import Product
from .forms import AddProductForm
from .cart import Cart

def add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    # 클라이언트 -> 서버로 데이터를 전달
    # 유효성 검사, injection 전처리
    form = AddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], is_update=cd['is_update'])

        return redirect('cart:detail')