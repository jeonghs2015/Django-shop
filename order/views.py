from django.shortcuts import render, get_object_or_404
from .models import *
from cart.cart import Cart
from .forms import *
# Create your views here.

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        # 입력받는 정보를 후처리
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.get_discount_total
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            cart.clear()
            return render(request, 'order/created.html', {'order':order})
    else:
        form = OrderCreateForm()
    return render(request, 'order/create.html', {'cart':cart,'form':form})

# JS가 동작하지 않는 환경에서도 주문은 가능해야합니다.
def order_complete(request):
    order_id = request.GET.get('order_id')
    order = Order.objects.get(id=order_id)
    get_object_or_404(Order, id=order_id)
    return render(request, 'order/created.html', {'order':order})


from django.views.generic.base import View
from django.http import JsonResponse


# 카트에서 제품 정보를 가져와 order 객체를 생성해주는 클래스
class OrderCreateAjaxView(View):
    def post(self, request, *args, **kwargs):
        # 로그인 하지 않은 회원은 403
        if not request.user.is_authenticated:
            return JsonResponse({"authenticated":False}, status=403)

        cart = Cart(request)
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.get_discount_total
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            cart.clear()
            data = {
                "order_id":order.id
            }
            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)

# 각 단계를 나눠서 처리하기위해 transaction을 나눠주기 위한 클래스
class OrderCheckoutAjaxView(View):
    def post(self, request, *args, **kwargs):
        # 로그인 하지 않은 회원은 403
        if not request.user.is_authenticated:
            return JsonResponse({"authenticated":False}, status=403)

        # order_id를 받아서 order 객체 만드는 부분
        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)

        amount = request.POST.get('amount')

        try:
            # transaction을 만들어서 merchant_order_id를 전달하는 목표
            merchant_order_id = OrderTransaction.objects.create_new(
                order=order,
                amount=amount
            )
        except:
            merchant_order_id = None

        if merchant_order_id is not None:
            data = {
                "works":True,
                "merchant_id":merchant_order_id
            }
            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)

# 후처리 클래스
# 제대로 된 order가 있는지 결제금액이 제대로 되어있는지 확인
class OrderImpAjaxView(View):
    def post(self, request, *args, **kwargs):
        # 로그인 하지 않은 회원은 403
        if not request.user.is_authenticated:
            return JsonResponse({"authenticated": False}, status=403)
        
        # order_id를 받아서 order 객체 만드는 부분
        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)

        merchant_id = request.POST.get('merchant_id')
        imp_id = request.POST.get('imp_id')
        amount = request.POST.get('amount')

        try:
            trans = OrderTransaction.objects.get(
                order=order,
                merchant_order_id=merchant_id,
                amount=amount
            )
        except:
            trans = None
        
        if trans is not None:
            trans.transaction_id = imp_id
            trans.save()
            order.paid = True
            order.save()

            data = {
                "works":True
            }            
            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)