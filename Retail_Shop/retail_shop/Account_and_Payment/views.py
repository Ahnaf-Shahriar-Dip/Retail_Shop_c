from django.shortcuts import render

from Product.md1 import *

from django.shortcuts import redirect

from django.utils import timezone
from django.shortcuts import render
from django.db import connection





def view_payment(request):
    queryset = Payment.objects.all()


    context = {'payments': queryset}
    return render(request, 'payment_info_view.html', context)







from django.db.models import Sum


def customer_account_view(request):
    # Retrieve all payments
    results = Payment.objects.all()

    # Retrieve the total amount for each customer_id from the Invoice model
    customer_totals = Invoice.objects.values('customer_id', 'customer_id__customer_name').annotate(
        total_amount=Sum('total')
    )

    # Retrieve the sum of payment amounts for each customer from the Payment model
    payment_totals = Payment.objects.values('customer_id').annotate(payment_total=Sum('payment_amount'))
    
    # Retrieve the sum of due amounts for each customer from the Payment model
    due_totals = Payment.objects.values('customer_id').annotate(due_total=Sum('due'))

    # Pass all sets of data to the template for rendering
    context = {
        'results': results,
        'customer_totals': customer_totals,
        'payment_totals': payment_totals,
        'due_totals': due_totals
    }
    return render(request, 'customer_account_view.html', context)

