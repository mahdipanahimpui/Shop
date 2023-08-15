from django.urls import path, include
from . import views

app_name = 'orders'


cart_urlpatterns = [
    path('', views.CartView.as_view(), name='cart'),
    path('add<int:product_id>', views.CartAddView.as_view(), name='cart_item_add'),
    path('remove/<int:product_id>', views.CartItemRemoveView.as_view(), name='cart_item_remove')
]

urlpatterns = [
    path('cart/', include(cart_urlpatterns))
]