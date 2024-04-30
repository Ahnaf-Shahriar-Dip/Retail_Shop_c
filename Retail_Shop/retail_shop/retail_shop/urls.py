"""
URL configuration for retail_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from home.views import *


from Staff_And_Cost.views import*
from Product.views import *
from Order.views import *
from Product_categories.views import *
from Customer.views import*
from Account_and_Payment.views import *
from Supplier.views import*
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    #path('' , home ,name="home"),
    path('add_product/',add_product,name="Receipe"),
    path('view_product/',view_product,name="Receipe"),
    


    path('add_product_category/',Product_categories,name="Receipe"),
    #path('view_product_category/',view_product_categories,name="Receipe"),



    path ('', login_page ,name="login_page"),


    path ('register/', register_page ,name="register_page"),

    path ('logout/', logout_page ,name="logout_page"),




    path ('product_delete/<product_id>/',    product_delete ,name="product_delete"),
    path ('product_update/<product_id>/', update_button ,name=" update_button"),


    path ('delete_Product_category/<category_id>/',   delete_Product_category ,name="delete_Product_category"),
    path ('update_Product_categories/<category_id>/', update_Product_categories ,name=" update_Product_categories"),

    


    

    path('admin/', admin.site.urls),

     path('login_page_user/', login_page_user, name='login_page_user'),


    path('cart_logic/', cart_logic, name='cart_logic'),

    path('view_customers/', view_customers, name='view_customers'),
    path('add_customer/', add_customer, name='add_customer'),


    path('View_Total_Sells/', View_Total_Sells, name='View_Total_Sells'),
    path('Actual_Sells/', Actual_Sells, name='Actual_Sells'),

    

    path('view_order_details_for_single_person/', view_order_details_for_single_person, name='view_order_details_for_single_person'),
   
   
    path('customer_with_highest_purchase/', customer_with_highest_purchase, name='view_order_details_for_single_person'),




    #path('cart/', view_cart, name='view_cart'),

    #path('payment_done/', payment_done, name='payment_done'),

    #path('delete_customer_orders/', Payment_DeleteCart_Create_Customeraccount, name='delete_customer_orders'),

    path('invoice_for_customers/', invoice_for_customers, name='invoice_for_customers'),

    #path('customer_acc/', customer_acc, name='customer_acc'),
    path('customer_account_view/', customer_account_view, name='customer_account_view'),




    path('add_Supplier/', Supplier_Create, name='add_Supplier'),
    path('view_supplier/', view_supplier, name='view_supplier'),


    path ('delete_Supplier/<int:supplier_id>/',   delete_Supplier ,name="delete_Supplier"),
    path ('update_supplier/<int:supplier_id>/', update_supplier ,name="update_supplier"),

    path('join/', join, name='join'),

    path('update_quantity/', update_quantity, name='update_quantity'),

    path('dip/', dip, name='dip'),

    path('sub_inv/', sub_inv, name='sub_inv'),

    path('sub_payment/', sub_payment, name='sub_payment'),

    
    
    path('staff/', staff, name='staff'),

    path ('delete_staff/<staff_id>/',   delete_staff ,name="delete_staff"),
    path ('update_staff/<staff_id>/', update_staff ,name=" update_staff"),

    path('add_expense/', add_expense, name='add_expense'),

    path ('delete_expense/<id>/',   delete_expense ,name="delete_expense"),
    path ('update_expense/<id>/', update_expense ,name=" update_expense"),
    path('invoice/', invoice_template, name='invoice_template'),
    

    path('view_payment/', view_payment, name='view_payment'),


    path('index/', index, name='index'),#home page

    



    path('user_list/', user_list, name='user_list'),
    path('update_user/<int:user_id>/', update_user, name='update_user'),

    
    
   

    

    
    
    


   











]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
