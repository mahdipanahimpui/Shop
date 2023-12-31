from django.urls import path, include
from . import views

app_name = 'home'

bucket_urlspattern = [
    path('', views.BucketHome.as_view(), name='bucket'),
    path('delete_obj_from_bucket/<path:key>', views.DeleteObjectFromBucketView.as_view(), name='delete_obj_from_bucket'),
    path('download_obj/<path:key>', views.DownloadObjectFromBucketView.as_view(), name='download_obj_from_bucket')
]

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('category/<slug:category_slug>', views.HomeView.as_view(), name='category_filter'),
    path('bucket/', include(bucket_urlspattern) ),
    
]

