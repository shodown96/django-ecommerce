from django.shortcuts import render, get_object_or_404, redirect
from core.models import Wishlist, Address
from django.core.paginator import Paginator
from .forms import ProfileForm, AddressForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.


@login_required
def dashboard(request):
    return render(request, 'vauth/dashboard.html')


@login_required
def wishlist(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    page = request.GET.get("page")
    paginator = Paginator(wishlist.items.all().order_by('title'), 10)
    items = paginator.get_page(page)
    context = {'wishlist': items}
    return render(request, "vauth/wishlist.html", context)


@login_required
def orders(request):
    order_list = request.user.order_set.all().order_by("-ordered_date")
    page = request.GET.get("page")
    paginator = Paginator(order_list, 10)
    orders = paginator.get_page(page)
    context = {'orders': orders}
    return render(request, "vauth/orders.html", context)


@login_required
def addresses(request):
    form = AddressForm()
    if request.POST:
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            if address.default:
                Address.objects.filter(
                    default=True, address_type=address.address_type).update(default=False)
            address.save()
            messages.success(request, "Successfully added new address")
        else:
            messages.error(request, form.errors, "danger")
        return redirect(request.META['HTTP_REFERER'])

    address_list = request.user.address_set.all()
    page = request.GET.get("page")
    paginator = Paginator(address_list, 10)
    addresses = paginator.get_page(page)
    context = {'addresses': addresses, 'form': form}
    return render(request, "vauth/addresses.html", context)


def profile(request):
    form = ProfileForm()
    if request.POST:
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        else:
            error = dict(form.errors)
            messages.error(request, error, extra_tags="danger")
    return render(request, 'vauth/profile.html', {'form': form})


def delete_address(request, ad_id):
    address = get_object_or_404(Address, id=ad_id)
    address.delete()
    messages.success(request, "Address has been deleted")
    return redirect(request.META['HTTP_REFERER'])


def edit_address(request, ad_id):
    if request.POST:
        address = get_object_or_404(Address, id=ad_id)
        form = AddressForm(data=request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully edited address")
        else:
            messages.error(request, form.errors, "danger")
        return redirect(request.META['HTTP_REFERER'])
