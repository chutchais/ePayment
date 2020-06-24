from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
# from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    print ('Add card %s' % product_id )
    cart = Cart(request)  # create a new cart object passing it the request object 
    # product = get_object_or_404(Product, id=product_id) 
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        print('Form valid')
        cd = form.cleaned_data

        # Validate from CMOS
        container   = cd['container']
        category      = 'E'
        full        = True
        oog         = False
        size        = 45
        # ------------------
        cart.add(container=container,category=category,size=size,
                full=full,oog=oog, quantity=1, update_quantity=cd['update'])
        # print('Valid form :',cart)
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    # product = get_object_or_404(Product, id=product_id)
    cart.remove(product_id)
    return redirect('create_order')


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    # print('cart_detail' , cart)
    # for item in cart:
    #     print(item)
        # print (item['quantity'])
        # item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'cart/detail.html', {'cart': cart})
