from django.shortcuts import render

from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from Product.md1 import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect




#def home(request):
    

    #return render(request,"home/Home_model.html",context={'page':'Django home page made by dip'})



def dip(request):
    

    return render(request,"home/dip.html",)
    








# for signup

from django.db import connection


def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username=request.POST.get('username')
        #email = request.post.get('email')
        password = request.POST.get('password')

        # Check if the user already exists
        user =User.objects.filter(username=username)
        if user.exists():
            messages.info(request, 'User Exist')

            return redirect('/register/')
        

        user=User.objects.create(



            first_name=first_name,
            last_name=last_name,
            username=username
            #email=email,
            
            
            )
        
        user.set_password(password)
        user.save()

        messages.info(request, 'Account created Successfully')
        return redirect('/')

    return render(request, 'home/register.html')









def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser:  # Check if the user is an admin
                return redirect('/index/')
            else:
                return redirect('/index/')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('/login/')

    return render(request, 'home/login.html')






def login_page_user(request):
    return render(request, 'home/Home_model_User.html')











def logout_page(request):
    request.session.clear()
    
    return redirect('/')




from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Min, Max



def index(request):
    today = timezone.now().date()
    
    # Calculate the sum of profit from the Invoice model
    profit_sum_today = Invoice.objects.filter(date_time__date=today).aggregate(profit_sum_today=Sum('profit'))['profit_sum_today'] or 0
    profit_sum_lifetime = Invoice.objects.aggregate(profit_sum_lifetime=Sum('profit'))['profit_sum_lifetime'] or 0

    # Calculate the sum of total from the Invoice model
    Sells_sum_today = Invoice.objects.filter(date_time__date=today).aggregate(Sells_sum_today=Sum('total'))['Sells_sum_today'] or 0
    Sells_sum_lifetime = Invoice.objects.aggregate(Sells_sum_lifetime=Sum('total'))['Sells_sum_lifetime'] or 0



    due_sum_today = Payment.objects.filter(payment_date__date=today).aggregate(due_sum_today=Sum('due'))['due_sum_today'] or 0
    due_sum_lifetime = Payment.objects.aggregate(due_sum_lifetime=Sum('due'))['due_sum_lifetime'] or 0


    expense_sum_today = Expense.objects.filter(date_time__date=today).aggregate(expense_sum_today=Sum('amount'))['expense_sum_today'] or 0
    expense_sum_lifetime = Expense.objects.aggregate(expense_sum_lifetime=Sum('amount'))['expense_sum_lifetime'] or 0


    net_earning_today=(Sells_sum_today-due_sum_today-expense_sum_today)+profit_sum_today
    net_earning_lifetime=(Sells_sum_lifetime-due_sum_lifetime -expense_sum_lifetime)+profit_sum_lifetime

    oldest_date = Invoice.objects.aggregate(oldest_date=Min('date_time'))['oldest_date']
    latest_date = Invoice.objects.aggregate(latest_date=Max('date_time'))['latest_date']





 # Execute raw MySQL query to get all products, ordered by product_name (descending) and product_quantity (descending)
    query = """
    SELECT * FROM product ORDER BY  Product_Quantity ASC
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        # Fetch all rows from the result set
        rows = cursor.fetchall()

    # Convert the raw query result to a list of dictionaries
    products = [{'product_quantity': row[3], 'product_name': row[1]} for row in rows]







    
 # Execute raw MySQL query to get all products, ordered by product_name (descending) and product_quantity (descending)
    query = """
        SELECT c.customer_name, SUM(p.due) AS total_due
        FROM payment p
        JOIN customers c ON p.customer_id = c.customer_id
        GROUP BY c.customer_name
        ORDER BY total_due DESC
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    # Convert the raw query result to a list of dictionaries
    customer_dues = [{'customer_name': row[0], 'total_due': row[1]} for row in rows]
    


    return render(request, 'home/Home_model.html', 
                  
                  {
                    'products': products,
                    'customer_dues':customer_dues,
                    'profit_sum_today': profit_sum_today,
                    'Sells_sum_today': Sells_sum_today, 
                    'due_sum_today': due_sum_today ,  
                    'expense_sum_today': expense_sum_today ,                         
                    'net_earning_today' :net_earning_today ,
                    'today_date':today ,

                    'profit_sum_lifetime':profit_sum_lifetime,
                    'Sells_sum_lifetime':Sells_sum_lifetime,
                    'due_sum_lifetime':due_sum_lifetime,
                    'expense_sum_lifetime':expense_sum_lifetime,

                    'net_earning_lifetime':net_earning_lifetime,
                    'oldest_date': oldest_date,
                    'latest_date': latest_date,
                      
                     
                     
                      })












