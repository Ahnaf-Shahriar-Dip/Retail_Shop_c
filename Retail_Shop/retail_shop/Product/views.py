
from django.shortcuts import render,redirect
from .md1 import *  #Importing models
from django.db import connection
from django.contrib.auth.decorators import login_required

#Creating product
from django.contrib import messages

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404



@login_required
#@staff_member_required


def add_product(request):
    if request.method == "POST":
        data = request.POST

        product_id = data.get('product_id')
        product_name = data.get('product_name')
        product_description = data.get('product_description')
        product_quantity = data.get('product_quantity')
        product_price = data.get("product_price")
        category_name = data.get('category_name')

        

        # Check if the category exists
        category = ProductCategories.objects.filter(category_name=category_name).first()

        #print(category.category_name)


        if not category:
            messages.error(request, 'Category does not exist')
            return redirect('/add_product/')

        # Create a new Product object
        new_product = Product(
            product_id=product_id,
            product_name=product_name,
            product_description=product_description,
            product_quantity=product_quantity,
            product_price=product_price,
            category_id=category
        )
        # Save the new product to the database
        new_product.save()

        # Update the product's category
       

        # Redirect to the add_product page
        return redirect('/view_product/')

    # Fetch all categories from the database
    categories = ProductCategories.objects.all()

    # Render the add_product template with the categories queryset
    return render(request, 'p/add_product.html', {'categories': categories})


#Product view 
def view_product(request):
    queryset = Product.objects.all()

    if request.GET.get('search'):
        search_term = request.GET.get('search')
        queryset = Product.objects.filter(product_name__icontains=search_term)

    context = {'products': queryset}
    return render(request, 'p/view_product.html', context)







#Delete product
def product_delete(request, product_id):
    with connection.cursor() as cursor:
        
        cursor.execute("DELETE FROM product WHERE product_id = %s", [product_id])

    return redirect('/view_product/')



# Product updating




def update_button(request, product_id):
    # Fetch the product from the database using Django's ORM
    product = Product.objects.get(product_id=product_id)

    if request.method == "POST":
        data = request.POST

        # Update the product attributes with the new data
        product.product_id = data.get('product_id')
        product.product_name = data.get('product_name')
        product.product_description = data.get('product_description')
        product.product_quantity = data.get('product_quantity')
        product.product_price = data.get('product_price')

        # Save the updated product to the database
        product.save()

        return redirect('/view_product/')

    context = {'results': product}
    return render(request, 'p/product_update.html', context)









               
    
    
    




from django.http import JsonResponse

def update_quantity(request):
    if request.method == "POST":
        data = request.POST
        product_id = data.get('product_id')
        new_quantity = int(data.get('new_quantity'))

        # Fetch the product from the database using Django's ORM
        product = Product.objects.get(product_id=product_id)
        
        # Increment the existing quantity with the new quantity
        product.product_quantity += new_quantity
        product.save()

        return JsonResponse({'success': True})  # You can customize the response as needed
    else:
        return JsonResponse({'success': False, 'error': 'Invalid Request'})








