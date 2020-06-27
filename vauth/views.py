from django.shortcuts import render
from core.models import Wishlist
from django.core.paginator import Paginator
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required

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
    address_list = request.user.address_set.all()
    page = request.GET.get("page")
    paginator = Paginator(address_list, 10)
    addresses = paginator.get_page(page)
    context = {'addresses': addresses}
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
