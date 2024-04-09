
from django.http import Http404
from django.shortcuts import render
from Product.md1 import *
from django.shortcuts import redirect
from django.contrib import messages
from django.db import connection
from django.shortcuts import get_object_or_404


def Product_categories(request):
    if request.method == "POST":
        data = request.POST

        category_id = data.get('category_id')
        category_name = data.get('category_name')
        

        # Check if category ID is duplicate
        count = ProductCategories.objects.filter(category_id=category_id).count()
        if count > 0:
            messages.error(request, 'Duplicate ID')
            return redirect('/add_product_category/')

        # Fetch the Product instance
        

        # Insert into ProductCategories table
        ProductCategories.objects.create(category_id=category_id, category_name=category_name)

        return redirect('/add_product_category/')
    

    queryset = ProductCategories.objects.all()

    # If search query parameter is present, filter the results
    search_query = request.GET.get('search')
    if search_query:
        queryset = queryset.filter(category_name__icontains=search_query)
    



    # Fetch all products
    

    context = {
        
        'Category': queryset,
    }

    return render(request, 'create.html', context)






#def view_product_categories(request):
   # queryset = ProductCategories.objects.select_related('product_id').all()

    # If search query parameter is present, filter the results
    #search_query = request.GET.get('search')
    #if search_query:
        #queryset = queryset.filter(category_name__icontains=search_query)

    #return render(request, 'view.html', {'Category': queryset})





def update_Product_categories(request, category_id):
    with connection.cursor() as cursor:
        # Fetch the existing product category based on category_id
        cursor.execute("SELECT * FROM product_categories WHERE category_id = %s", [category_id])
        queryset = cursor.fetchone()

        
        if request.method == "POST":
            data = request.POST

            new_category_id = data.get('category_id')
            new_category_name = data.get('category_name')

            # Update the product category
            cursor.execute(
                "UPDATE product_categories SET category_id = %s, category_name = %s WHERE category_id = %s",
                [new_category_id, new_category_name, category_id]
            )

            return redirect('/add_product_category/')

    context = {'Product_fun': queryset}
    return render(request, 'Category_update.html', context)







def delete_Product_category(request, category_id):
    with connection.cursor() as cursor:
        # Delete the product category based on category_id
        cursor.execute("DELETE FROM product_categories WHERE category_id = %s", [category_id])

    return redirect('/add_product_category/')



