import weasyprint
from celery import shared_task

from django.core.mail import send_mail, EmailMessage
from io import BytesIO
from django.template.loader import render_to_string

from .models import Order


@shared_task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Order number {order.id}'
    message = f'Dear {order.first_name}, \n\n' \
        f'Your order was successfully created. \n' \
        f'Your order ID is {order.id}'

    # mail_sent = send_mail(
    #     subject,
    #     message,
    #     'elegance@store.store',
    #     [order.email]
    # )
    # return mail_sent

    email = EmailMessage(
        subject,
        message,
        'elegance@store.store',
        [order.email]
    )
    # generate pdf
    html = render_to_string('order/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets = []
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
    # attach PDF file
    email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')


@shared_task
def status_change_notification(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Order number {order.id}'
    message = f'Dear {order.first_name}, \n\n' \
              f'Status of your order {order.id} was changed to {order.status}'

    mail_sent = send_mail(
        subject,
        message,
        'elegance@store.store',
        [order.email]
    )
    return mail_sent
