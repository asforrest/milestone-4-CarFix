from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderLineItem

from subscriptions.models import Subscription
from cart.contexts import cart_contents

import stripe
import json

@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'cart': json.dumps(request.session.get('cart', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)

def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        cart = request.session.get('cart', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'country': request.POST['country'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save()(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            order.save()
            for item_id, item_data in cart.items():
                try:
                    subscription = Subscription.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            subscription=subscription,
                            quantity=item_data,
                        )
                        order_line_item.save()

                except Subscription.DoesNotExist:
                    messages.error(request, (
                        "One of the subscriptions in your cart wasn't "
                        "found in our database. "
                        "Please contact us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_cart'))

            # Save the info to the user's profile if all is well
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success',
                                    args=[order.order_number]))
        else:
            messages.error(request, ('There was an error with your form. '
                                     'Please double check your information.'))
    else:

        current_cart = cart_contents(request)
        total = current_cart['total']

        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )


        order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. ')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51IXHjKHjJQjzesItIzWaWTHYcsYDfOsvFsKLoGNqYr9jQTKpvD40zbIOKJydQLyQLSahXx50FjmsB8uRQh1S4dbM00bhoLcHvu',
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)

def checkout_success(request, order_number):
    # Handle successful checkouts
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'cart' in request.session:
        del request.session['cart']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)