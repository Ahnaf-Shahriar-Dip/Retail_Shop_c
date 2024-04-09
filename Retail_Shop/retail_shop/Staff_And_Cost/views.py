from django.shortcuts import render



from django.http import Http404
from django.shortcuts import render
from Product.md1 import *
from django.shortcuts import redirect
from django.contrib import messages
from django.db import connection
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required



from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.contrib.auth.models import User



from django.contrib.admin.views.decorators import superuser_required


@login_required

@superuser_required


def staff(request):
    if request.method == "POST":
        data = request.POST

        
        staff_name = data.get('staff_name')
        salary = data.get('salary')
        phone_Number = data.get('phone_number')
        address = data.get('address')

        

        # Insert into Staff table
        Staff.objects.create(
            
            
            staff_name=staff_name, 
            salary=salary,
            phone_Number=phone_Number,
            address=address
                                  
                    )

        return redirect('/staff/')
    
    queryset = Staff.objects.all()
    

    # If search query parameter is present, filter the results
    search_query = request.GET.get('search')
    if search_query:
        queryset = queryset.filter(staff_name__icontains=search_query)
    
    context = {
        'Staffs': queryset
    }

    return render(request, 'create_staff.html', context)







def delete_staff(request, staff_id):
    with connection.cursor() as cursor:
        # Delete the product category based on category_id
        cursor.execute("DELETE FROM staff WHERE Staff_Id = %s", [staff_id])

    return redirect('/staff/')




def update_staff(request, staff_id):
    with connection.cursor() as cursor:
        # Fetch the existing staff based on staff_id

        if request.method == "POST":
            data = request.POST

            new_staff_name = data.get('staff_name')
            new_salary = data.get('salary')
            new_phone_number = data.get('phone_number')
            new_address = data.get('address')

            # Update the staff record
            cursor.execute(
                "UPDATE staff SET Staff_Name = %s, Salary = %s, Phone_Number = %s, Address = %s WHERE Staff_Id = %s",
                [new_staff_name, new_salary, new_phone_number, new_address, staff_id]
            )

            return redirect('/staff/')
        
        # Retrieve the existing staff record
        cursor.execute("SELECT * FROM staff WHERE Staff_Id = %s", [staff_id])
        staff = cursor.fetchone()

    # Pass the retrieved staff record to the template context
    context = {
        'staff': staff
    }

    return render(request, 'staff_update.html', context)


















from django.utils import timezone
def add_expense(request):
    if request.method == "POST":
        data = request.POST

        
        expense_for = data.get('expense_for')
        amount = data.get('amount')
        date_time = data.get('date_time')

        date_time = timezone.datetime.strptime(date_time, '%Y-%m-%dT%H:%M')
        

        

        # Insert into Staff table
        Expense.objects.create(
            
            
            expense_for=expense_for, 
           
            amount=amount,
            date_time=date_time
                                  
                    )

        return redirect('/add_expense/')
    
    queryset = Expense.objects.all()
    

   
    
    context = {
        'expenses': queryset
    }

    return render(request, 'create_expense.html', context)






def delete_expense(request, id):
    with connection.cursor() as cursor:
        
        cursor.execute("DELETE FROM expense WHERE Id = %s", [id])

    return redirect('/add_expense/')








def update_expense(request, id):
    with connection.cursor() as cursor:
        

        if request.method == "POST":
            data = request.POST

            new_expense_for = data.get('expense_for')
            new_amount = data.get('amount')

            
            cursor.execute(
                "UPDATE expense SET expense_for = %s, Amount= %s WHERE Id = %s",
                [new_expense_for, new_amount, id]
            )

            return redirect('/add_expense/')
        
        
        cursor.execute("SELECT * FROM expense WHERE Id = %s", [id])
        expense = cursor.fetchone()

    
    context = {
        'expense': expense
    }

    return render(request, 'expense_update.html', context)











from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

def update_user(request, user_id):
    if request.method == 'POST':
        action = request.POST.get('action')
        user = User.objects.get(pk=user_id)
        
        if action == 'toggle_staff':
            user.is_staff = not user.is_staff
            user.save()
            messages.success(request, f"Staff status for {user.username} updated successfully.")
        
        elif action == 'toggle_admin':
            user.is_superuser = not user.is_superuser
            user.save()
            messages.success(request, f"Admin status for {user.username} updated successfully.")
        
        return redirect('user_list')

    else:
        return redirect('user_list')

def user_list(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'user_list.html', context)


def update_user(request, user_id):
    if request.method == 'POST':
        action = request.POST.get('action')
        user = User.objects.get(pk=user_id)
        
        if action == 'toggle_staff':
            # Toggle staff status
            user.is_staff = not user.is_staff
            user.save()
            messages.success(request, f"Staff status for {user.username} updated successfully.")
        
        elif action == 'toggle_admin':
            # Toggle admin status
            user.is_superuser = not user.is_superuser
            user.save()
            messages.success(request, f"Admin status for {user.username} updated successfully.")
        
        elif action == 'delete':
            # Delete user
            user.delete()
            messages.success(request, f"{user.username} has been deleted successfully.")
        
        return redirect('user_list')

    else:
        return redirect('user_list')