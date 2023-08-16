from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, OrderItem
from django.views import View
from .cart import Cart
from home.models import Product
from .forms import CartAddForm



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

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(request, self.template_name, {'order': order})



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
