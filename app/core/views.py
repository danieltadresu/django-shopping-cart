from django.shortcuts import render

from core.models import Product, Order
from core.forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
# Create your views here.

import stripe
stripe.api_key = 'sk_test_51HQlYBKVWRemJMNbYdPyEEGInMoFLN9MwF1UA0m6rxk8o97VVB4jS5B4LXBjNN8XGeVXWiBjcNTT1NqIin9I1HJj00LtxiIU4C'

def getIndex(request):
    fetchAllProducts = Product.objects.all()
    data = {
        'products': fetchAllProducts
    }
    return render(request, 'index.html', data)

@permission_required('core.view_product')
def getCheckout(request, id):
    product = Product.objects.get(productId=id)
    print('My product -> ', product.price )
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
              'price_data': {
                'currency': 'clp',
                'unit_amount': product.price,
                'product_data': {
                  'name': product.title,
                 },
               },
                 'quantity': 1,
             },
            ],
            mode='payment',
            success_url='http://localhost:8000/success/' + str(id),
            cancel_url='http://localhost:8000',
        )
    return render(request, 'products/checkout-products.html', {'id': checkout_session.id})

def getSuccessPay(request, id):
    fetchProduct = Product.objects.get(productId=id)
    Order.objects.create(
        product = fetchProduct
    )
    return render(request, 'index.html')

def registro(request):

    data = {
        'form': CustomUserCreationForm
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data['username'], password=formulario.cleaned_data['password1'])
            login(request, user)
            return render(request, 'index.html', data)
        data['form'] = formulario
    return render(request, 'registration/registro.html', data)
