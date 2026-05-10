from ftplib import all_errors
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from decimal import Decimal
import razorpay
import json
import random
import string

from .models import *


def home(request):
    products = Products.objects.all()
    return render(request, 'homepage.html', {'products': products})


def product(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    return render(request, 'product.html', {'product': product})


def about(request):
    return render(request, 'about_us.html')


def contact(request):
    return render(request, 'contact.html')



def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    subtotal = Decimal('0')
    total_items = 0

    for item in cart.values():
        product = get_object_or_404(Products, id=item['product_id'])
        qty = item['quantity']
        price = Decimal(str(item['price']))
        item_total = price * qty

        subtotal += item_total
        total_items += qty

        cart_items.append({
            'product': product,
            'quantity': qty,
            'price': price,
            'item_total': item_total,
        })

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'total': subtotal,
        'total_items': total_items
    })


def add_to_cart(request):
    if request.method != 'POST':
        return redirect('cart')

    product_id = request.POST.get('productid')
    quantity = int(request.POST.get('quantity', 1))
    product = get_object_or_404(Products, id=product_id)

    cart = request.session.get('cart', {})
    pid = str(product_id)

    if pid in cart:
        cart[pid]['quantity'] += quantity
    else:
        cart[pid] = {
            'product_id': product.id,
            'name': product.product_name,
            'price': float(product.product_price),
            'image': product.product_img_url or '',
            'quantity': quantity,
        }

    request.session['cart'] = cart
    request.session.modified = True

    total_items = sum(item['quantity'] for item in cart.values())
    subtotal = sum(item['price'] * item['quantity'] for item in cart.values())
    total = subtotal

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'{product.product_name} added to cart',
            'total_items': total_items,
            'cart_data': {
                'total_items': total_items,
                'subtotal': subtotal,
                'total': total
            }
        })

    return redirect('cart')


from django.http import JsonResponse

def remove_from_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        removed = cart.pop(str(product_id), None)
        request.session['cart'] = cart
        request.session.modified = True

        total_items = sum(item['quantity'] for item in cart.values())
        subtotal = sum(item['price'] * item['quantity'] for item in cart.values())
        total = subtotal  # free shipping

        # Check AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if removed:
                return JsonResponse({
                    'success': True,
                    'message': 'Item removed from cart',
                    'cart_data': {
                        'total_items': total_items,
                        'subtotal': subtotal,
                        'total': total
                    }
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Item not found in cart',
                    'cart_data': {
                        'total_items': total_items,
                        'subtotal': subtotal,
                        'total': total
                    }
                })

    return redirect('cart')

def clear_cart(request):
    request.session.pop('cart', None)
    return redirect('cart')


def get_cart_count(request):
    cart = request.session.get('cart', {})
    count = sum(item['quantity'] for item in cart.values())
    return JsonResponse({'count': count})


def buy_now(request):
    if request.method != 'POST':
        return redirect('home')

    product_id = request.POST.get('productid')
    quantity = int(request.POST.get('quantity', 1))
    product = get_object_or_404(Products, id=product_id)

    request.session['cart'] = {
        str(product_id): {
            'product_id': product.id,
            'name': product.product_name,
            'price': float(product.product_price),
            'quantity': quantity,
        }
    }

    return redirect('checkout')


from django.utils import timezone
from decimal import Decimal

def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart')

    cart_items = []
    subtotal = Decimal('0')

    for item in cart.values():
        price = Decimal(str(item['price']))
        qty = item['quantity']
        item_total = price * qty
        subtotal += item_total

        cart_items.append({
            'product_id': item['product_id'],
            'name': item['name'],
            'price': price,
            'quantity': qty,
            'item_total': item_total
        })

    total = subtotal

    if request.method == 'GET':
        return render(request, 'checkout.html', {
            'cart_items': cart_items,
            'subtotal': subtotal,
            'total': total,
            'state_choices': STATE_CHOICES,
            'country_choices': COUNTRY_CHOICES,
            'current_date': timezone.now().date(),
        })

    data = request.POST
    payment_method = data.get('payment_method')

    address = Address.objects.create(
        address=data.get('address'),
        apartment_suite=data.get('apartment_suite', ''),
        city=data.get('city'),
        state=data.get('state'),
        country=data.get('country'),
        pin_code=data.get('pin_code'),
    )

    order = Order.objects.create(
        customer=data.get('customer'),
        phone=data.get('phone'),
        email=data.get('email'),
        address=address,
        total_amount=total,
        payment_method=payment_method,
        payment_status='pending',
        paid_amount=Decimal('0')
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product_id=item['product_id'],
            quantity=item['quantity'],
            price=item['price']
        )

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    payable_amount = total
    if payment_method == 'cod':
        payable_amount = total * Decimal('0.2')

    razorpay_order = client.order.create({
        'amount': int(payable_amount * 100),
        'currency': 'INR',
        'payment_capture': 1
    })

    order.razorpay_order_id = razorpay_order['id']
    order.save()

    return JsonResponse({
        'success': True,
        'razorpay_key': settings.RAZORPAY_KEY_ID,
        'razorpay_order_id': razorpay_order['id'],
        'amount': int(payable_amount * 100),
        'order_id': order.id,
        'payment_method': payment_method
    })


@csrf_exempt
def verify_payment(request):
    data = json.loads(request.body)
    order = get_object_or_404(Order, id=data['order_id'])

    if order.payment_method != 'cod':
  
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': data['razorpay_order_id'],
                'razorpay_payment_id': data['razorpay_payment_id'],
                'razorpay_signature': data['razorpay_signature']
            })
        except:
            return JsonResponse({'success': False, 'error': 'Payment verification failed'})
        order.payment_status = 'completed'
        order.paid_amount = order.total_amount

    else:
       
        order.payment_status = 'partial'
        order.paid_amount = order.total_amount * Decimal('0.2')  # ✅ this sets 20% advance

    order.save() 
    request.session.pop('cart', None)

    return JsonResponse({'success': True, 'redirect_url': f'/order-success/{order.id}/'})


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Get order items
    order_items_queryset = OrderItem.objects.filter(order=order)
    order_items = []

    for item in order_items_queryset:
        order_items.append({
            'product': item.product,
            'quantity': item.quantity,
            'price': item.price,
            'item_total': item.price * item.quantity,
        })

    cod_advance = Decimal('0')
    balance_on_delivery = Decimal('0')

    if order.payment_method == 'cod' and order.payment_status == 'partial':
        cod_advance = order.paid_amount
        balance_on_delivery = order.total_amount - order.paid_amount

    context = {
        'order': order,
        'order_items': order_items,
        'cod_advance': cod_advance,
        'balance_on_delivery': balance_on_delivery,
    }

    return render(request, 'order_success.html', context)


ADMIN_PASSWORD = "vi.jix@25#11"


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('admin_authenticated'):
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return wrapper

@admin_required
def admin_login(request):
    if request.method == 'POST':
        if request.POST.get('admin_password') == ADMIN_PASSWORD:
            request.session['admin_authenticated'] = True
            return redirect('admin_dashboard')
        messages.error(request, 'Wrong password')
    return render(request, 'admin_login.html')




@admin_required
def admin_dashboard(request):
    
    all_orders = Order.objects.all().order_by('-created_at')
    
    for order in all_orders:
        if order.payment_method == 'cod':
            if order.payment_status == 'partial':
                order.dynamic_paid = order.total_amount * Decimal('0.2')
                order.dynamic_balance = order.total_amount - order.dynamic_paid
            elif order.payment_status == 'completed':
                order.dynamic_paid = order.total_amount
                order.dynamic_balance = Decimal('0.0')
            else:  # pending
                order.dynamic_paid = Decimal('0.0')
                order.dynamic_balance = order.total_amount
        else:  # Razorpay / online payment
            order.dynamic_paid = order.paid_amount or Decimal('0.0')
            order.dynamic_balance = order.total_amount - order.dynamic_paid


    recent_orders = all_orders[:10]

    total_revenue = sum(o.dynamic_paid for o in all_orders)
    total_orders = all_orders.count()
    today = timezone.now().date()
    today_orders = all_orders.filter(created_at__date=today).count()
    month_orders = all_orders.filter(created_at__month=today.month).count()
    total_balance = sum(o.dynamic_balance for o in all_orders)

    stats = {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'today_orders': today_orders,
        'month_orders': month_orders,
        'total_balance': total_balance,
    }

    context = {
        'recent_orders': recent_orders,
        'stats': stats,
    }

    return render(request, 'admin_dashboard.html', context)




@admin_required
def order_detail_admin(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    order_items_queryset = OrderItem.objects.filter(order=order)
    
    order_items = []
    for item in order_items_queryset:
        product = item.product  
        order_items.append({
            'product': product,
            'quantity': item.quantity,
            'price': item.price,
            'item_total': item.quantity * item.price,
        })
    
    cod_advance = 0
    balance_due = 0
    if order.payment_method == 'cod' and order.payment_status == 'partial':
        cod_advance = float(order.total_amount) * 0.2
        balance_due = float(order.total_amount) - cod_advance
    
    context = {
        'order': order,
        'order_items': order_items,
        'cod_advance': cod_advance,
        'balance_due': balance_due
    }
    
    
    return render(request, 'admin_order_detail.html', context)



def admin_logout(request):
    request.session.flush()
    return redirect('admin_login')

from django.shortcuts import render, get_object_or_404
from decimal import Decimal
from .models import Order

from decimal import Decimal

def print_shipping_label(request, order_id):
    order = Order.objects.get(id=order_id)

    balance_amount = Decimal('0.00')
    if order.payment_method == 'cod' and order.payment_status != 'completed':
       
        balance_amount = (order.total_amount * Decimal('0.8')).quantize(Decimal('0.01'))

    total_items = sum(item.quantity for item in order.items.all())

    context = {
        'order': order,
        'balance_amount': balance_amount,
        'total_items': total_items
    }
    return render(request, 'shipping_label.html', context)


from django.shortcuts import render
from .models import Order

def print_all_orders(request):
    orders = Order.objects.all() 
    return render(request, 'bulk_shipping_labels.html', {'orders': orders})


from django.shortcuts import render
from store.models import Order
from django.utils.dateparse import parse_date


def print_orders_by_date(request):
    date_str = request.GET.get('date') 
    if date_str:
        date_obj = parse_date(date_str)
        if date_obj:
            orders = Order.objects.filter(created_at__date=date_obj)
           
            for order in orders:
                order.balance_amount = order.total_amount - order.paid_amount if order.payment_status != 'completed' else 0
        else:
            orders = []
    else:
        orders = []

    return render(request, 'bulk_shipping_labels.html', {'orders': orders})


def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    order_items_queryset = OrderItem.objects.filter(order=order)
    
    order_items = []
    for item in order_items_queryset:
        product = item.product  
        order_items.append({
            'product': product,
            'quantity': item.quantity,
            'price': item.price,
            'item_total': item.quantity * item.price,
        })
    
    
    cod_advance = 0
    balance_due = 0
    if order.payment_method == 'cod' and order.payment_status == 'partial':
        cod_advance = float(order.total_amount) * 0.2
        balance_due = float(order.total_amount) - cod_advance
    
    context = {
        'order': order,
        'order_items': order_items,
        'cod_advance': cod_advance,
        'balance_due': balance_due
    }
    return render(request, 'order_details.html', context)

# views.py
from django.shortcuts import render
from .models import Order

def print_orders_selected(request):
    ids = request.GET.get('ids', '')
    if ids:
        id_list = [int(i) for i in ids.split(',')]
        orders = Order.objects.filter(id__in=id_list)
        for order in orders:
            order.balance_amount = order.total_amount - order.paid_amount if order.payment_status != 'completed' else 0
    else:
        orders = []
    return render(request, 'bulk_shipping_labels.html', {'orders': orders})

def print_all_orders(request):
    orders = Order.objects.all()
    orders_with_balance = []

    for order in orders:
        balance_amount = Decimal('0.00')
        if order.payment_method == 'cod' and order.payment_status != 'completed':
        
            balance_amount = (order.total_amount * Decimal('0.8')).quantize(Decimal('0.01'))
        orders_with_balance.append((order, balance_amount))

    return render(request, 'bulk_shipping_labels.html', {'orders_with_balance': orders_with_balance})


def print_orders_by_date(request):
    date_str = request.GET.get('date')
    if date_str:
        from django.utils.dateparse import parse_date
        date_obj = parse_date(date_str)
        if date_obj:
            orders = Order.objects.filter(created_at__date=date_obj)
        else:
            orders = []
    else:
        orders = []

    orders_with_balance = []
    for order in orders:
        balance_amount = Decimal('0.00')
        if order.payment_method == 'cod' and order.payment_status != 'completed':
            balance_amount = (order.total_amount * Decimal('0.8')).quantize(Decimal('0.01'))
        orders_with_balance.append((order, balance_amount))

    return render(request, 'bulk_shipping_labels.html', {'orders_with_balance': orders_with_balance})