

# Create your views here.
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.db import connection
from Product.md1 import *



#Create Done

def Supplier_Create(request):
    if request.method == "POST":
        data = request.POST

        supplier_id = data.get('Supplier_Id')
        supplier_name = data.get('Supplier_Name')
        phone_number = data.get('Phone_number')

        

        if Supplier.objects.filter(supplier_id=supplier_id).exists():
            messages.error(request, 'Duplicate supplier ID')
            return redirect('/add_Supplier/')


        with connection.cursor() as cursor:
            # Create and execute the raw SQL query
            cursor.execute(
                "INSERT INTO supplier (Supplier_Id, Supplier_Name, Phone_number) VALUES (%s, %s, %s)",
                [supplier_id, supplier_name, phone_number]


            )



        return redirect('/add_Supplier/')

    return render(request, 'Supplier_create.html')

        





    
               
#Done
    
def view_supplier(request):
    with connection.cursor() as cursor:
        # Execute the raw SQL query to retrieve all products
        cursor.execute("SELECT * FROM supplier")

        queryset = cursor.fetchall()

    if request.GET.get('search'):
        # Execute the raw SQL query to filter results based on the search term
        search_term = request.GET.get('search')
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM supplier WHERE LOWER(Supplier_Name) LIKE %s", ['%' + search_term.lower() + '%'])
            queryset = cursor.fetchall()

    context = {'results': queryset}
    return render(request, 'supplier_view.html', context)






def join(request):
    with connection.cursor() as cursor:
        # Execute the raw SQL query to retrieve the product
        cursor.execute("SELECT p.product_id, p.product_name, p.product_description, s.supplier_id, s.supplier_name, s.phone_number FROM  product p JOIN supplier s ON p.product_id = s.supplier_id;"
    )
        
        supplier = cursor.fetchall()

        
   
    context = {'results': supplier}
    return render(request, 'join.html', context)






#Done
def update_supplier(request, supplier_id):
    with connection.cursor() as cursor:
        # Execute the raw SQL query to retrieve the product
        cursor.execute("SELECT * from supplier WHERE  Supplier_Id = %s", [supplier_id])
        supplier = cursor.fetchone()

    if request.method == "POST":
        data = request.POST

        supplier_id = data.get('Supplier_Id')
        supplier_name = data.get('Supplier_Name')
        phone_number =  data.get('Phone_number')
        

        with connection.cursor() as cursor:
            # Execute the raw SQL query to update the product

            cursor.execute(
            "UPDATE supplier SET Supplier_Name = %s, Phone_number = %s WHERE Supplier_Id = %s",
            [supplier_name, phone_number, supplier_id]
)
            

        return redirect('/view_supplier/')

    context = {'results': supplier}
    return render(request, 'supplier_update.html', context)





#Done
def delete_Supplier(request, supplier_id):
    with connection.cursor() as cursor:
        # Execute the raw SQL query to delete the supplier
            cursor.execute("DELETE FROM supplier WHERE  Supplier_Id = %s", [supplier_id])

    return redirect('/view_supplier/')

