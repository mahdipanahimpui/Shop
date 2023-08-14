from django.urls import path, include
from . import views

app_name = 'home'

bucket_urlspattern = [
    path('', views.BucketHome.as_view(), name='bucket'),
    path('delete_obj_from_bucket/<path:key>', views.DeleteObjectFromBucketView.as_view(), name='delete_obj_from_bucket'),
]

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('bucket/', include(bucket_urlspattern) )
    
]

