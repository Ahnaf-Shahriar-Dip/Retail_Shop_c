
from django.shortcuts import render, redirect
from Product.md1 import *
from django.db import connection

def add_customer(request):
    if request.method == 'POST':
        # Get data from the request
        customer_id = request.POST.get('customer_id')
        customer_name = request.POST.get('customer_name')
        customer_address = request.POST.get('customer_address')
        customer_phone = request.POST.get('customer_phone')
        customer_email = request.POST.get('customer_email')

        with connection.cursor() as cursor:
            # Create and execute the raw SQL query
            cursor.execute(
                "INSERT INTO customers (customer_id, customer_name, customer_address, customer_phone, customer_email) VALUES (%s, %s, %s, %s, %s)",
                [customer_id, customer_name, customer_address, customer_phone, customer_email]
            )

        return redirect('/view_customers/')

    return render(request, 'add_customer.html')


def view_customers(request):
    with connection.cursor() as cursor:
        # Execute the raw SQL query to retrieve all customers
        cursor.execute("SELECT * from customers")
        customers = cursor.fetchall()

    context = {'results': customers}

    return render(request, 'view_customers.html', context)



def invoice_for_customers(request):
    if request.method == 'GET':
        order_date = request.GET.get('order_date')
        customer_id = request.GET.get('customer_id')

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    c.Customer_Id,
                    c.Customer_Name,
                    c.Customer_Address,
                    c.Customer_Phone,
                    o.Order_Id,
                    o.Product_Id,
                    p.Product_Name,
                    o.Quantity,
                    o.Per_Kg_Price,
                    o.Subtotal,
                    o.Order_Date,

                    SUM(o.Subtotal) OVER (PARTITION BY c.Customer_Id) AS Total_Subtotal
                FROM
                    Customers c
                JOIN
                    Orders o ON c.Customer_Id = o.Customer_Id
                JOIN
                    Product p ON o.Product_Id = p.Product_Id
                WHERE
                    DATE(o.Order_Date) = %s
                    AND c.Customer_Id = %s;
            """, 
            [order_date, customer_id])

            results = cursor.fetchall()

        return render(request, 'invoice.html', {'results': results})


