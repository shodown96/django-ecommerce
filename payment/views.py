from django.shortcuts import render, redirect, resolve_url
from django.http import Http404
import random
import string
import datetime
# from .models import Payment
from django.contrib import messages
import requests
import json
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from core.forms import CheckoutForm, CouponForm, RefundForm
from core.models import Item, OrderItem, Order, Address, Coupon, Refund, UserProfile, Payment
from django.core.exceptions import ObjectDoesNotExist

paystack_api = settings.PAYSTACK_API


def ref_code():
    url = "https://api.paystack.co/transaction"
    references = []
    reference = "".join(random.choices(
        string.ascii_lowercase + string.digits + string.ascii_uppercase, k=20))
    headers = {
        'Authorization': 'Bearer ' + paystack_api,
        # 'Cookie': '__cfduid=d1d572f045715bf5e3ac13529693ddf181589112047; sails.sid=s%3AGN2W-h4g7UcXTAqWFRA5BXiedYd-62M8.tRfWMbVx1CWHNVj1qxu9eCpnxPUhZM%2FxbiQWnbX8vWo'
    }
    response = requests.request("GET", url, headers=headers)
    r = response.json()
    for x in r['data']:
        references.append(x['reference'])
    if reference in references:
        reference = "". join(set(reference))
    print(references)
    return reference


def pay(request):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        amount = int(order.get_total() * 100)

        url = "https://api.paystack.co/transaction/initialize"
        current_site = get_current_site(request)
        domain = current_site.domain
        payload = {
            "email": request.user.email,
            "amount": amount,
            "currency": "NGN",
            "callback_url": f"http://{domain}/payment/callback/verify/",
            "metadata": {
                "cancel_action": f"http://{domain}/payment/cancel/"
            }
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + paystack_api,
        }

        response = requests.request(
            "POST", url, headers=headers, data=json.dumps(payload))

        # print(response.text.encode('utf8'), '\n')
        r = response.json()
        print(json.dumps(r, indent=4))
        if r['status']:
            payment = Payment(
                status="abandoned",
                user=request.user,
                email=request.user.email,
                amount=amount,
                access_code=r['data']['access_code'],
                authorization_url=r['data']['authorization_url'],
                reference=r['data']['reference']
            ).save()
            # payment.save()

            return redirect(r['data']['authorization_url'])
        elif r['message'] == "Duplicate Transaction Reference":
            # payment = Payment.objects.get(reference=reference)
            # if payemnt.status == "abandoned":
            return redirect(payment.authorization_url)
        else:
            messages.error(
                request, "Oops, seems like something went wrong, please try again later, thank you", extra_tags="danger")
            return redirect(request.META['HTTP_REFERER'])
    except ObjectDoesNotExist:
        messages.error(self.request, "You do not have an active order")
        return redirect(request.META['HTTP_REFERER'])


def verify_payment(request, payment_id):
    if verify(request, payment_id):
        messages.success(
            request, "Payment Accepted, Thank you so much for your support.")
    else:
        messages.warning(
            request, "Donation could not be proccessed at this time, but don't worry we would handle it and inform you about it later")
    return redirect('core:home')


def callback(request):
    txref = request.GET.get('txref')
    reference = request.GET.get('reference')
    if txref == reference:
        print("\ntxref = reference\n")
    payment = Payment.objects.get(reference=reference)
    if verify(request, payment.id):
        messages.success(
            request, "Payment Accepted, Thank you so much for your support.")
    else:
        messages.warning(
            request, "Payment could not be proccessed at this time, but don't worry we would handle it and inform you about it later")
    return redirect('core:home')


def cancel(request):
    payment = Payment.objects.filter(user=request.user, status="abandoned")[0]
    payment.delete()
    messages.info(request, "Changed your mind? No problem.")
    return redirect('core:home')


def verify(request, payment_id):
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    payment = Payment.objects.get(id=payment_id)
    message = False
    url = f"https://api.paystack.co/transaction/verify/{payment.reference}"

    headers = {
        'Authorization': 'Bearer ' + paystack_api,
    }

    response = requests.request("GET", url, headers=headers)

    print(response.text.encode('utf8'), '\n')
    r = response.json()
    print(json.dumps(r, indent=4))
    if response.status_code == 200:
        payment.status = r['data']['status']
        payment.api_id = r['data']['id']
        payment.status = r['data']['status']
        payment.reference = r['data']['reference']
        payment.created_at = datetime.datetime.fromisoformat(
            r['data']['created_at'][:-1] + "+00:00")
        if r['data']['status'] == "success":
            payment.paid = True
            payment.paid_at = datetime.datetime.fromisoformat(
                r['data']['paid_at'][:-1] + "+00:00")
            if order_qs.exists():
                order = order_qs[0]
                order_items = order.items.all()
                order_items.update(ordered=True)
                for item in order_items:
                    item.save()

                order.ordered = True
                order.payment_id = payment.id
                order.ref_code = r['data']['reference']
                order.save()
            message = True
        payment.save()
    return message


# "http://127.0.0.1:8000/payment/callback/verify"
