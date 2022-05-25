from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Order, OrderItems

from .tasks import status_change_notification


def status_change(queryset, status):
    for order in queryset:
        order.status = status
        order.save()
        status_change_notification.delay(order.id)


def status_processing(modeladmin, request, queryset):
    status_change(queryset, 'Processing')


status_processing.short_description = 'status_processing'


def status_shipped(modeladmin, request, queryset):
    status_change(queryset, 'Shipped')


status_shipped.short_description = 'status_shipped'



def order_pdf(obj):
    return format_html('<a href="{}">PDF</a>', reverse('orders:invoice_pdf', args=[obj.id]))


order_pdf.short_description = 'Invoice'


class OrderItemInline(admin.TabularInline):
    model = OrderItems


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = [
        'id', 'first_name', 'last_name', 'email',
        'address', 'postal_code', 'city',
        'state', 'transport', 'created', 'status', order_pdf
    ]
    list_filter = ['created', 'updated']
    inlines = [OrderItemInline]

    actions = [status_processing, status_shipped]