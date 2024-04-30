from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from datetime import datetime, timezone
from Product.md1 import *      #Importing models which is inside Product app/Directory
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


from django.core.exceptions import ObjectDoesNotExist
from django.db import models


import json




@csrf_exempt
def cart_logic(request):
    if request.method == 'GET':
        # Query all products and customers from the database
        products = Product.objects.all()
        customers = Customers.objects.all()

        # Pass the products and customers to the template
        return render(request, 'sells_product.html', {'products': products, 'customers': customers})

    elif request.method == 'POST':
        try:
            # Extract data from the request body (JSON)
            data = json.loads(request.body.decode('utf-8'))  # Decode the bytes and parse JSON

            # Iterate over each order data object
            for order_data in data:
                # Fetch the Customers instance based on the provided customer_id
                customer = Customers.objects.get(pk=order_data.get('customer_id'))
                product = Product.objects.get(pk=order_data.get('product_id'))

                quantity = order_data.get('quantity')

                if product.product_quantity < quantity:
                    return JsonResponse({'error': 'Insufficient stock for product: {}'.format(product.product_name)}, status=400)
                
                product_price = product.product_price
                per_kg_price = order_data.get('per_kg_price')
                profit = (per_kg_price-product_price)* quantity
                



                # Create a new Orders object and save it to the database
                order = Orders.objects.create(
                    product_id=product,
                    customer_id=customer,  # Assign the Customers instance
                    per_kg_price=order_data.get('per_kg_price'),
                    quantity=order_data.get('quantity'),
                    subtotal=order_data.get('subtotal'),
                    order_date=order_data.get('order_date'),
                    invoice_id=order_data.get('invoice_id'),
                    profit=profit
                )

                product.product_quantity -= quantity
                product.save()
                order.save()

                #Null Isuue sometimes when storing sum of profit in invoice table 

                #print("Order object created:", order)  # Debugging statement

                 # Aggregate profit for orders with the same invoice ID
            order_profits = Orders.objects.values('invoice_id').annotate(total_profit=Sum('profit'))
            

            # Update the corresponding invoice records with aggregated profit
            for order_profit in order_profits:
                invoice_id = order_profit['invoice_id']
                total_profit = order_profit['total_profit']
                Invoice.objects.filter(invoice_id=invoice_id).update(profit=total_profit)
                

            # Return a success response
            return JsonResponse({'message': 'Orders and invoice submitted successfully'}, status=200)
        except Exception as e:
            # Return an error response if something goes wrong
            print("Error:", e)  # Debugging statement
            return JsonResponse({'error': str(e)}, status=500)
    else:
        # Return a method not allowed response for other HTTP methods
        return JsonResponse({'error': 'Method not allowed'}, status=405)




from django.db.models import Sum
from django.utils import timezone





@csrf_exempt
def sub_inv(request):
    if request.method == 'POST':
        try:
            # Decode the JSON data sent from the client
            data = json.loads(request.body.decode('utf-8'))

            # Extract invoice information from the data
            shipping_cost = data.get('shipping_cost')
            labour_cost = data.get('labour_cost')
            vat = data.get('vat')
            discount = data.get('discount')
            total = data.get('total')
            invoice_id = data.get('invoice_id')  # Get the invoice_id from the request data
            customer_id = data.get('customer_id')
            

            # Print the invoice information for debugging
            #print("Shipping Cost:", shipping_cost)
            #print("Labour Cost:", labour_cost)
            #print("VAT:", vat)
            #print("Discount:", discount)
            #print("Total:", total)

            customer = Customers.objects.get(pk=customer_id)


            invoice = Invoice.objects.create(
                shipping_cost=shipping_cost,
                labour_cost=labour_cost,
                vat=vat,
                discount=discount,
                total=total,
                invoice_id=invoice_id,
                customer_id=customer,
                date_time=timezone.now()  
            )

             # Query the Orders table to get the profit for the current invoice
            #order_profit = Orders.objects.filter(invoice_id=invoice_id).aggregate(Sum('profit'))
            #total_profit = order_profit['profit__sum'] or 0  # If no profit found, default to 0

            # Update the invoice with the total profit
            #invoice.profit = total_profit
            invoice.save()


            # Return a success response
            return JsonResponse({'message': 'Invoice data received successfully'}, status=200)
        except Exception as e:
            # Return an error response if something goes wrong
            print("Error:", e)  # Debugging statement
            return JsonResponse({'error': str(e)}, status=500)
    else:
        # Return a method not allowed response for other HTTP methods
        return JsonResponse({'error': 'Method not allowed'}, status=405)







@csrf_exempt
def sub_payment(request):
    if request.method == 'POST':
        try:
            # Decode the JSON data sent from the client
            data = json.loads(request.body.decode('utf-8'))

            # Extract invoice information from the data
            payment_amount = data.get('payed')
            due = data.get('due')
            pay_method = data.get('pay_method')
            change_amount = data.get('change_amount')

            invoice_id = data.get('invoice_id')  
            customer_id = data.get('customer_id')
            payment_date=data.get('order_date')


           
            

          

            customer = Customers.objects.get(pk=customer_id)

            payment = Payment.objects.create(
                payment_amount=payment_amount,
                due=due,
                pay_method=pay_method,
                change_amount=change_amount,
                invoice_id=invoice_id,
                customer_id=customer,
                payment_date=payment_date
            )

            
            payment.save()

            


            # Return a success response
            return JsonResponse({'message': 'Payment data received successfully'}, status=200)
        except Exception as e:
            # Return an error response if something goes wrong
            print("Error:", e)  # Debugging statement
            return JsonResponse({'error': str(e)}, status=500)
    else:
        # Return a method not allowed response for other HTTP methods
        return JsonResponse({'error': 'Method not allowed'}, status=405)











def Actual_Sells(request):
    cursor = connection.cursor()

    # Execute the query to get all details from the invoice table
    cursor.execute(
        """
        SELECT invoice.*, customers.customer_name
        FROM invoice
        INNER JOIN customers ON invoice.Customer_Id = customers.Customer_Id
        """
    )
    order_details = cursor.fetchall()

    # Execute the query to get the total subtotal for each invoice
    cursor.execute(
        """
        SELECT Invoice_Id, SUM(Subtotal) AS Total_Subtotal
        FROM orders
        GROUP BY Invoice_Id
        """
    )
    invoice_details = cursor.fetchall()

    cursor.close()

    # Pass the fetched data to the template for rendering
    return render(request, 'actual_Sells.html', {'order_details': order_details, 'invoice_details': invoice_details})











def invoice_template(request):
    # Retrieve data from query parameters
    shipping_cost = request.GET.get('shippingCost')
    labour_cost = request.GET.get('labourCost')
    vat_amount = request.GET.get('vatAmount')
    discount = request.GET.get('discount')
    total = request.GET.get('total')
    payed = request.GET.get('payed')
    change_amount = request.GET.get('changeAmount')
    due = request.GET.get('due')
    payment_method = request.GET.get('paymentMethod')

    # Render the invoice template with the data
    return render(request, 'invoice_template.html', {
        'shipping_cost': shipping_cost,
        'labour_cost': labour_cost,
        'vat_amount': vat_amount,
        'discount': discount,
        'total': total,
        'payed': payed,
        'change_amount': change_amount,
        'due': due,
        'payment_method': payment_method,
    })














def View_Total_Sells(request):
    cursor = connection.cursor()

    cursor.execute(
            """
            SELECT 
                o.Order_Id,
                c.customer_name,
                o.Invoice_Id,
                c.customer_address,
                c.customer_email,
                p.product_name,
                o.Quantity,
                o.Per_Kg_Price,
                o.Subtotal,
                o.Order_Date
                
            FROM 
                orders o
            INNER JOIN 
                product p ON o.Product_Id = p.product_id
            INNER JOIN 
                customers c ON o.Customer_Id = c.customer_id
            ORDER BY
                o.Order_Id ASC
            """
        )
    order_details = cursor.fetchall()

    
    cursor.close()
    return render(request, 'view_Totall_sell_details.html', {'order_details': order_details})






def customer_with_highest_purchase(request):
    query = '''
        SELECT c.Customer_Id, c.Customer_Name, c.Customer_Address, c.Customer_Phone, c.Customer_Email, 
               SUM(p.Totall) AS total_purchase
        FROM Customers c
        JOIN invoice p ON c.Customer_Id = p.Customer_Id
        GROUP BY c.Customer_Id, c.Customer_Name, c.Customer_Address, c.Customer_Phone, c.Customer_Email
        ORDER BY Totall DESC
    '''
    with connection.cursor() as cursor:
        cursor.execute(query)
        customer_info = cursor.fetchall()  

    customer_list = []  # Convert fetched rows to a list of dictionaries
    for row in customer_info:
        customer_dict = {
            'customer_id': row[0],
            'customer_name': row[1],
            'customer_address': row[2],
            'customer_phone': row[3],
            'customer_email': row[4],
            'total_purchase': row[5],
        }
        customer_list.append(customer_dict)

    return render(request, 'customer_highest_purchase.html', {'customer_info': customer_list})

    








    








#----------------------NOT NaEEDD--------------

from django.db import connection
from django.shortcuts import render

def view_order_details_for_single_person(request):
    # Write a raw SQL query to fetch the most recent order with customer details
    query = '''
        SELECT p.Order_Id, p.Product_Name, c.Customer_Name, p.Quantity, p.Per_kg_price, p.Subtotal
        FROM Orders p
        JOIN customers c ON p.Customer_ID = c.Customer_ID
        ORDER BY p.Order_Id DESC
        LIMIT 1
    '''
    with connection.cursor() as cursor:
        cursor.execute(query)
        latest_order = cursor.fetchone()

    # Assuming 'latest_order' is a tuple, you can convert it to a dictionary for convenience
    order_dict = {
        'Order_Id': latest_order[0],
        'product_name': latest_order[1],
        'customer_name': latest_order[2],
        'quantity': latest_order[3],
        'per_kg_price': latest_order[4],
        'subtotal': latest_order[5],
    }

    return render(request, 'view_One_order_details.html', {'order_details': [order_dict]})




#---------------------------------------------------------------------------------------------






