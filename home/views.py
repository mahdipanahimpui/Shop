from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Product
from . tasks import all_bucket_objects_task

class HomeView(View):
    template_name = 'home/home.html'

    def get(self, request):
        products = Product.objects.filter(available=True)
        return render(request, self.template_name, {'products': products})
        
        

class ProductDetailView(View):
    template_name = 'home/detail.html'

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        return render(request, self.template_name, {'product': product})





class BucketHome(View):
    template_name = 'home/bucket.html'

    # dispatch method runs befor all methods in class
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            return redirect('home:home')
        # return super is required if code is continued
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        objects = all_bucket_objects_task() # is it is asynck use .dealy() or apply_async

        return render(request, self.template_name, {'objects': objects})