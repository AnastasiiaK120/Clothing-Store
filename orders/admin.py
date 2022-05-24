from django.contrib import admin
from .models import Order, OrderItems


def status_change(queryset, status):
    for order in queryset:
        order.status = status
        order.save()


def status_processing(modeladmin, request, queryset):
    status_change(queryset, 'Processing')


status_processing.short_description = 'status_processing'


def status_shipped(modeladmin, request, queryset):
    status_change(queryset, 'Shipped')


status_shipped.short_description = 'status_shipped'


class OrderItemInline(admin.TabularInline):
    model = OrderItems


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = [
        'id', 'first_name', 'last_name', 'email',
        'address', 'postal_code', 'city',
        'state', 'transport', 'created', 'status'
    ]
    list_filter = ['created', 'updated']
    inlines = [OrderItemInline]

    actions = [status_processing, status_shipped]