from django.shortcuts import render, get_object_or_404, redirect
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

