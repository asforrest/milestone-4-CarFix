from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages

from subscriptions.models import Subscription

# Create your view


def view_cart(request):
    # View to return the contents of the shopping cart page
    return render(request, 'cart/cart.html')


def add_to_cart(request, item_id):
    if request.POST.get('quantity') == "":
        return redirect(reverse('subscription_detail', args=[item_id]))

    # View to add quantity to the shopping cart
    subscrption = get_object_or_404(Subscription, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})


    if item_id in list(cart.keys()):
        cart[item_id] += quantity
        messages.success(request,
                            (f'Updated {subscrption.name} '
                            f'quantity to {cart[item_id]}'))
    else:
        cart[item_id] = quantity
        messages.success(request, f'Added {subscrption.name} to your cart')

    request.session['cart'] = cart
    return redirect(redirect_url)


def adjust_cart(request, item_id):
    if request.POST.get('quantity') == "":
        return redirect(reverse('view_cart'))


    # Adjust the quantity of subscriptions
    subscription = get_object_or_404(Subscription, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})
    print(quantity)


    if quantity > 0:
        cart[item_id] = quantity
        messages.success(request,
                            (f'Updated {subscription.name} '
                            f'quantity to {cart[item_id]}'))
    else:
        cart.pop(item_id)
        messages.success(request,
                            (f'Removed {subscription.name} '
                            f'from your cart'))

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))


def remove_from_cart(request, item_id):
    try:
        # Remove item from shopping cart
        subscription = get_object_or_404(Subscription, pk=item_id)
        cart = request.session.get('cart', {})
        cart.pop(item_id)
        messages.success(request, f'Removed {subscription.name} from your cart')

        request.session['cart'] = cart
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
