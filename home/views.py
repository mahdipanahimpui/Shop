from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Product
from . import tasks
from django.contrib import messages
from utils import IsAdminUserMixin

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





class BucketHome(IsAdminUserMixin, View):
    template_name = 'home/bucket.html'

    # # dispatch method runs befor all methods in class
    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.is_admin:
    #         return redirect('home:home')
    #     # return super is required if code is continued
    #     return super().dispatch(request, *args, **kwargs)
    # *** dispatch is not required by overwriting the UserPassesTestMixin in utils.py *****

    def get(self, request):
        objects = tasks.all_bucket_objects_task() # is it is asynck use .dealy() or apply_async

        return render(request, self.template_name, {'objects': objects})
    

class DeleteObjectFromBucketView(IsAdminUserMixin, View):
    
    def get(self, request, key):
        delete_result = tasks.delete_object_task.delay(key) # run rabbitmq and run the celery -A Shop worker -l info  in env
        messages.success(request, 'your object will delete soon ...', 'info')
        delete_result.get() # app wait until the result getting, it is not required
        return redirect('home:bucket')
    


class DownloadObjectFromBucketView(IsAdminUserMixin, View):

    def get(self,request, key):
        tasks.download_object_task.delay(key)
        messages.success(request, 'download will stating soon', 'info')
        return redirect('home:bucket')
