from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, OrderItem
from django.views import View
from .cart import Cart
from home.models import Product
from orders.models import Coupon
from . forms import CouponApplyForm
from .forms import CartAddForm
from django.contrib import messages
from django.conf import settings
import requests
import json
from django.http import HttpResponse
from django.http import JsonResponse
import datetime
import pytz




class CartView(View):
    template_name = 'orders/cart.html'

    def get(self, request):
        cart = Cart(request)
        return render(request, self.template_name, {'cart': cart})
    


class CartAddView(View):
    from_class = CartAddForm
    template_name = 'home/detail.html'


    def get(self, request):
        pass

    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product, cd['quantity'])
            return redirect('orders:cart')
    
        return render(request, self.template_name, {'product': product, 'form': form})
    

class CartItemRemoveView(View):

    def get(self, request, product_id):
        cart = Cart(request)
        cart.cart_item_remvoe(product_id)
        return redirect('orders:cart')
    


class OrderDetailView(LoginRequiredMixin, View):
    template_name = 'orders/order.html'
    form_class = CouponApplyForm

    def get(self, request, order_id):
        form = self.form_class
        order = get_object_or_404(Order, id=order_id)
        return render(request, self.template_name, {'order': order, 'form':form})



class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)

        cart_list = list(cart)
        product_ids = [int(item['product_id']) for item in cart_list]

        products = Product.objects.filter(id__in=product_ids)

        for item, product in zip(cart_list, products):
            OrderItem.objects.create(order=order, product=product, price=item['price'], quantity=item['quantity'])

        cart.clear_cart()

        return redirect('orders:order_detail', order.id)
    



## zarrinpall payment all of them is wrong
sandbox = 'www'

MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXX-XX-XX'
ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
CallbackURL = 'http://127.0.0.1:8080/orders/verify/'


class OrderPayView(LoginRequiredMixin, View):

    def get(self, request, order_id):
        order = Order.objects.get(id=order_id)
        request.session['order_pay'] = {
            'order_id': order.id
        }

        data = {
            "MerchantID": MERCHANT,
            "Amount": order.get_total_cost(),
            "Description": description,
            "Phone": request.user.phone_number,
            "CallbackURL": CallbackURL,
        }
        data = json.dumps(data)

        headers = {'content-type': 'application/json', 'content-length': str(len(data))}

        try:
            response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

            if response.status_code == 200:
                response_data = response.json()
                if response_data['Status'] == 100:
                    redirect_url = ZP_API_STARTPAY + str(response_data['Authority'])
                    authority = response_data['Authority']

                    # Create a JSON response with the desired data
                    json_response = {
                        'status': True,
                        'url': redirect_url,
                        'authority': authority
                    }

                    # Set the X-Frame-Options header in the JSON response
                    json_response["X-Frame-Options"] = self.get_xframe_options_value()

                    return JsonResponse(json_response)
                else:
                    return redirect('orders:order_verify')
                    # return JsonResponse({'status': False, 'code': str(response_data['Status'])})
            return response

        except requests.exceptions.Timeout:
            return JsonResponse({'status': False, 'code': 'timeout'})
        except requests.exceptions.ConnectionError:
            return JsonResponse({'status': False, 'code': 'connection error'})


class OrederVerifyView(LoginRequiredMixin, View):
    def get(self, request):
        order_id = request.session['order_pay']['order_id']
        order = Order.objects.get(id=int(order_id))
        order.paid = True
        order.save()
        messages.success(request, ' paid ok', 'success')
        return redirect('orders:cart')
    



class CouponApplyView(LoginRequiredMixin, View):
    form_class = CouponApplyForm
    template_name = 'orders/order.html'


    def post(self, request, order_id):
        now = datetime.datetime.now(tz=pytz.timezone('Asia/Tehran'))
        order = Order.objects.get(id=order_id)
        form = self.form_class(request.POST)

        if form.is_valid():
            code = form.cleaned_data['code']
            try: 
                coupon = Coupon.objects.get(code__exact=code, valid_from__lte=now, valid_to__gte=now, active=True)

            except Coupon.DoesNotExist:
                messages.error(request, 'this coupon does not exitst', 'danger')
                return render(request, self.template_name, {'order': order, 'form':form})

            order.discount = coupon.discount
            order.save()
        
        return redirect('orders:order_detail', order_id)
                


        