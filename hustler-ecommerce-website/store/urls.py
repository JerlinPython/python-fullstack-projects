from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
 
    path('', views.home, name='home'),
    path('product/<int:product_id>/', views.product, name='product_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    path('cart/', views.cart, name='cart'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('cart/count/', views.get_cart_count, name='cart_count'),

    path('buy-now/', views.buy_now, name='buy_now'),
    path('checkout/', views.checkout, name='checkout'),
    path('verify-payment/', views.verify_payment, name='verify_payment'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),

    path('dashboard/login/', views.admin_login, name='admin_login'),
    path('dashboard/logout/', views.admin_logout, name='admin_logout'),
    path('dashboard/orders/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/order/<int:order_id>/', views.order_detail_admin, name='order_detail_admin'),
    path('print-shipping-label/<int:order_id>/', views.print_shipping_label, name='print_shipping_label'),
    path('print-all-orders/', views.print_all_orders, name='print_all_orders'),
    path('print-orders-by-date/', views.print_orders_by_date, name='print_orders_by_date'),
    path('dashboard/print_orders_by_date/', views.print_orders_by_date, name='print_orders_by_date'),
    path('dashboard/print_all_orders/', views.print_all_orders, name='print_all_orders'),
    path('dashboard/print_orders_selected/', views.print_orders_selected, name='print_orders_selected'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
