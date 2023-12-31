from django.urls import path, include
from . import views

app_name = 'orders'


cart_urlpatterns = [
    path('', views.CartView.as_view(), name='cart'),
    path('add<int:product_id>', views.CartAddView.as_view(), name='cart_item_add'),
    path('remove/<int:product_id>', views.CartItemRemoveView.as_view(), name='cart_item_remove')
]



urlpatterns = [
    path('cart/', include(cart_urlpatterns)),
    path('create/', views.OrderCreateView.as_view(), name='orders_create'),
    path('detail/<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('pay/<int:order_id>', views.OrderPayView.as_view(), name='order_pay'),
    path('verify/', views.OrederVerifyView.as_view(), name='order_verify'),
    path('apply_coupon/<int:order_id>', views.CouponApplyView.as_view(), name='apply_coupon')
]
