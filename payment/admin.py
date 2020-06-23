from django.contrib import admin
from core.models import Payment
from .views import verify
from django.contrib import messages
# Register your models here.


def admin_verify_payment(modeladmin, request, queryset):
    count = 0
    abandoned = []
    for x in queryset:
        if verify(request, x.id):
            count += 1
            x.paid = True
        else:
            abandoned.append(x.email)
    negcount = queryset.count() - count
    if count > 0:
        messages.success(request, str(count) + ' Payments were successful')
        messages.warning(request, str(negcount) +
                         ' Payments were abandoned or unsuccessful')


admin_verify_payment.short_description = "Verify Payments"


def delete_abandoned_payment(modeladmin, request, queryset):
    count = 0
    deleted = queryset.filter(status="abandoned")
    count = deleted.count()
    deleted.delete()

    if count > 0:
        messages.success(request, f"Deleted {str(count)} abandoned payments")
    else:
        messages.info(request, "No abandoned payments found")


delete_abandoned_payment.short_description = "Delete Abandoned Payments"


class PaymentAdmin(admin.ModelAdmin):
    actions = [admin_verify_payment, delete_abandoned_payment]
    list_display = ['user', 'amount', 'paid_at', 'status', 'reference']
    list_filter = ['amount', 'status']


admin.site.register(Payment, PaymentAdmin)
