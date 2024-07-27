from django.shortcuts import render , redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.db.models import Count
from datetime import date
from django.contrib.auth.models import User
from .models import shipment,route,package,supplier,warehouse 
from .models import customer,location,payment,ship
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
from .forms import SignUpForm , UpdateUserForm
import json
from django.utils import timezone
from decimal import Decimal
import requests 
from django.db.models import Count
import json






def page1(request):
    if request.method == "POST":
        company = request.POST["company"]
        phone_number = request.POST["phone_number"]

        customer.objects.create(
            company=company,
            phone_number=phone_number
        )
        return redirect('confirmation')
    else:
        return render(request, 'redundant.html')

def home(request):
    return render(request,'home.html',{})

def about(request):
    return render(request ,'about.html',{})
def contact(request):
    return render(request ,'contact.html',{})

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:  # Ensure both username and password are provided
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('admin_dash')  # Redirect to admin dashboard
                else:
                    return redirect('card')  # Redirect to user dashboard
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Please provide both username and password")
    return render(request, 'login.html')  # Render the login page for GET requests

def logout_user(request):
    logout(request)
    messages.success(request,("you have logged out"))
    return redirect('home')


def shipment_details(request):
    if request.method == "POST":
        company = request.POST["company"]
        uid = request.POST["uid"]
        customer_obj = customer.objects.get(uid=uid)
        if customer_obj and customer_obj.company == company:
            shipments = shipment.objects.filter(cust=customer_obj)
            data = {
                "shipments": shipments,
                "customer": customer_obj,  
            }
            return render(request, "show_shipment_result.html", data)
        else:
            messages.error(request, "Invalid company name or UID.")
            return render(request, "card.html")
    else:
        cust=customer.objects.all()
        return render(request, "shipments.html",{'cust':cust})    

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance = current_user)

        if user_form.is_valid():
            user_form.save()

            login(request,current_user)
            messages.success(request,"User has been updated successfully")
            return redirect('card')
        return render(request,"update_user.html",{'user_form':user_form})
    else:
        messages.success(request,"you must be logged in to access ")
        return redirect('home')
    

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Authenticate and login the user
            login(request, user)
            messages.success(request, "You have registered successfully.")
            return redirect('login')  
        else:
            messages.error(request, "Registration was unsuccessful.")
    else:
        form = SignUpForm()
     
    return render(request, 'register.html', {'form': form})


def card(request):
    return render(request,'card.html',{})

def admin_dash(request):
    return render(request,'admin_dash.html',{})

def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

def update_tables(request):
    return render(request,'update_tables.html',{})


def edit_user(request, user_id):
    user = User.objects.get(pk=user_id)
    last_login = user.last_login

    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if a new password was provided before changing it
        if password:
            user.password = make_password(password)

        user.is_superuser = 'is_superuser' in request.POST

        user.save()

        # If the password was changed, update the session hash to keep the user logged in.
        if password:
            update_session_auth_hash(request, user)

        return redirect('user_list')

    return render(request,'edit_user.html',{'user': user,'last_login': last_login})




def toggle_user_status(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = not user.is_active
    user.save()
    return redirect('user_list')

def add_tables(request):
    return render(request,'add_tables.html',{})


def page2(request):
    if request.method == "POST":
        departure = request.POST["departure_date"]
        arrival = request.POST["arrival_date"]
        cust = request.POST["cust"]
        cust_instance = customer.objects.get(company=cust)
        routes = request.POST["routes"]
        rout = route.objects.get(name=routes)
        ships = request.POST["ships"]
        shipss = ship.objects.get(ship_name=ships)
        packs = request.POST["pack"]
        pack = package.objects.get(contents=packs)

        shipment.objects.create(
            departure_date=departure,
            arrival_date=arrival,
            cust=cust_instance,
            routes=rout,
            ships=shipss,
            package=pack,
        )
        return redirect('view_shipments')
    else:
        cust = customer.objects.all()
        routes = route.objects.all()
        ships = ship.objects.all()
        packages = package.objects.all()
        return render(request, 'add_shipments.html', {'cust': cust, 'routes': routes, 'ships': ships,'packages': packages})
    
def page3(request):
    if request.method == "POST":
        ship_name = request.POST["ship_name"]
        ship_type = request.POST["ship_type"]
        capacity = request.POST["capacity"]

        ship.objects.create(
            ship_name=ship_name,
            ship_type=ship_type,
            capacity=capacity
        )
        return redirect('add_tables')
    else:
        return render(request, 'add_ship.html')    
    
def page4(request):
    if request.method == "POST":
        name =request.POST["name"]
        duration = request.POST["duration"]
        distance = request.POST["distance"]
        destinations = request.POST["destination"]
        destination = location.objects.get(city=destinations)
        startlocations = request.POST["startlocation"]
        startlocation = location.objects.get(city=startlocations)

        route.objects.create(
            name=name,
            duration=duration,
            distance=distance,
            destination=destination,
            startlocation=startlocation
        )
        return redirect('add_tables')
    else:
        loc = location.objects.all()
        return render(request, 'add_route.html',{'loc':loc})    
    
def page5(request):
    if request.method == "POST":
        warehouse_name= request.POST["warehouse_name"]
        capacity = request.POST["capacity"]

        warehouse.objects.create(
            warehouse_name=warehouse_name,
            capacity=capacity
        )
        return redirect('add_tables')
    else:
        return render(request, 'add_warehouse.html')   

def page6(request):
    if request.method == "POST":
        name = request.POST["name"]
        phone = request.POST["phone"]

        supplier.objects.create(
            name=name,
            phone=phone
        )
        return redirect('add_tables')
    else:
        return render(request, 'add_supplier.html')    

def page7(request):
    if request.method == "POST":
        amounts = request.POST["amount_in_crores"]
        cu = request.POST["company_name"]
        c = customer.objects.get(company=cu)

        payment.objects.create(
            amount_in_crores=amounts,
            company_name=c
        )
        return redirect('add_tables')
    else:
        c = customer.objects.all()
        return render(request, 'add_payments.html',{'c':c})    

def page8(request):
    if request.method == "POST":
        city = request.POST["city"]
        country = request.POST["country"]

        location.objects.create(
            city=city,
            country=country
        )
        return redirect('add_tables')
    else:
        return render(request, 'add_location.html') 


def page9(request):
    if request.method == "POST":
        contents = request.POST["contents"]
        supp = request.POST["sup"]
        sup = supplier.objects.get(name=supp)
        wares = request.POST["ware"]
        ware = warehouse.objects.get(warehouse_name=wares)
        package.objects.create(
            contents=contents,
            sup=sup,
            ware=ware
        )
        return redirect('add_tables')
    else:
        sup = supplier.objects.all()
        ware = warehouse.objects.all()
        return render(request, 'add_package.html',{'sup':sup,'ware':ware})      
    
def delete_customer(request):
    if request.method == 'POST':
        company = request.POST["company"]
        customers = customer.objects.filter(company=company)
        for i in customers:
            i.delete()
            messages.success(request,"Customer has been deleted successfully")
        else:
            return render(request,'admin_dash.html')
    cust=customer.objects.all()    
    return render(request, 'delete_customer.html',{'cust':cust})

def view_shipments(request):
    all_shipments = shipment.objects.all()
    data={
        'all_shipments': all_shipments
    }
    return render(request, "view_shipments.html", data)

def confirmation(request):
    all_customers = customer.objects.all()
    data={
       'all_customers': all_customers
    }  
    return render(request,'confirmation.html',data)


def shipment_view(request):
    if request.method == "POST":
        company = request.POST["company"]
        uid = request.POST["uid"]
        customer_obj = customer.objects.get(uid=uid)
        if customer_obj and customer_obj.company == company:
            user_shipment_count = shipment.objects.filter(cust_id= company).count()
            cust_id_counts = shipment.objects.values('cust_id').annotate(count=Count('cust_id'))

            total_shipment_count = shipment.objects.count()
            total_user_count = shipment.objects.values('cust_id').distinct().count()
            average_shipment_count = total_shipment_count / total_user_count

            context = {
            'user_shipment_count': user_shipment_count,
            'average_shipment_count': average_shipment_count,
            'cust_id_counts' : cust_id_counts,
            }
            return render(request, "user_dashboard.html", context)
        else:
            messages.error(request, "Invalid company name or UID.")
            return render(request, "card.html")
    else:
        cust=customer.objects.all()
        return render(request, "shipment_view.html",{'cust':cust})

def barchart(request):
    cust_id_counts = shipment.objects.values('cust_id').annotate(count=Count('cust_id'))
    cust_id_counts_json = json.dumps(list(cust_id_counts))
    data = {
        'cust_id_counts' : cust_id_counts,
        'cust_id_counts_json' : cust_id_counts_json,
    }
    return render(request, "barchart.html", data)


def current_shipments(request):
    current_shipments = shipment.objects.filter(arrival_date__gt=timezone.now().date())
    
    context = {
        'current_shipments': current_shipments,
    }

    return render(request,'current_shipment.html',context)

def view_location(request):
    all_location = location.objects.all()
    data={
       'all_location': all_location
    }  
    return render(request,'view_location.html',data)

def view_ship(request):
    all_ship = ship.objects.all()
    data={
       'all_ship': all_ship
    }  
    return render(request,'view_ship.html',data)

def calculate_shipping_rate(request):
    if request.method == 'POST':
        weight = request.POST.get('weight')
        region = request.POST.get('region')
        if weight and region:
            shipping_rate = calculate_rate(weight, region)
            return render(request, 'shipping_rate.html', {'rate': shipping_rate})
        else:
            return render(request, 'shipping_calculator.html', {'error_message': 'Weight and region are required.'})
    else:
        return render(request, 'shipping_calculator.html')


def calculate_rate(weight, region):
    base_rate = Decimal('10')  # Base rate for shipping
    rate_per_kg = Decimal('2')  # Rate per kilogram of weight
    if region == 'Local':
        distance = Decimal('50')  # Local distance range in kilometers
    elif region == 'Domestic':
        distance = Decimal('500')  # Domestic distance range in kilometers
    elif region == 'International':
        distance = Decimal('5000')  # International distance range in kilometers
    else:
        distance = Decimal('0')  # Default distance if region is not specified
    rate_per_km = Decimal('0.1')  # Rate per kilometer of distance

    total_rate = base_rate + (rate_per_kg * Decimal(weight)) + (rate_per_km * distance)
    return total_rate


def ship_routes_news(request):
    api_key = 'Your api key'
    query = 'cargo ships maritime shipping' 
    url = f'http://newsapi.org/v2/everything?q={query}&apiKey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        articles = data['articles']
        return render(request, 'ship_routes.html', {'articles': articles})
    else:
        messages.error(request, "Failed to retrieve news articles.")
        return render(request,"card.html")        

def route_analysis(request):
    route_shipments = shipment.objects.values('routes').annotate(count=Count('routes'))

    if route_shipments:
        # Find the maximum count among all routes
        max_count = max(route_shipments, key=lambda x: x['count'])['count']

        # Filter the routes with the maximum count
        max_count_routes = [route['routes'] for route in route_shipments if route['count'] == max_count]

        # Display a success message with the route names
        if len(max_count_routes) == 1:
            messages.success(request, f"The route with the maximum count is: {max_count_routes[0]}")
        else:
            messages.success(request, f"The routes with the maximum count are: {', '.join(max_count_routes)}")
    else:
        # Display a message indicating no shipments found
        messages.success(request, "No shipments found.")

    return render(request, 'route_analysis.html', {'route_shipments': route_shipments})
   
def update_customer(request):
    if request.method == 'POST':
        company = request.POST.get("company")
        phone = request.POST.get("phone")  # Updated phone number
        
        # Check if the customer exists
        data = customer.objects.get(company=company)
        if data:
            # Update the phone number
            data.phone_number = phone
            data.save()  # Save the changes to the database
            messages.success(request, "Customer details have been updated successfully")
        else:
            messages.error(request, "Customer does not exist")
        
        return redirect('update_tables') 
    else:
        customers = customer.objects.all()
        return render(request, 'update_customer.html', {'customers': customers})

    

def update_ship(request):
    if request.method == 'POST':
        ship_name = request.POST.get("ship_name")
        ship_type = request.POST.get("ship_type")
        capacity = request.POST.get("capacity")
        
        ship_obj = ship.objects.get(ship_name=ship_name)
        if ship_obj:
            ship_obj.ship_type = ship_type
            ship_obj.capacity = capacity
            ship_obj.save()
            messages.success(request, "Ship details have been updated successfully")
        else:
            messages.error(request, "Ship does not exist")
        return redirect('update_tables')  # Redirect to update_tables or wherever needed
    else:
        ships = ship.objects.all()
        return render(request, 'update_ship.html', {'ships': ships})   

def update_ware(request):
    if request.method == 'POST':
        warehouse_name = request.POST.get("warehouse_name")
        capacity = request.POST.get("capacity")
        # Check if the customer exists
        data = warehouse.objects.get(warehouse_name=warehouse_name)
        if data:
            data.capacity = capacity
            data.save() 
            messages.success(request, "Warehouse details have been updated successfully")
        else:
            messages.error(request, "Warehouse does not exist")
        
        return redirect('update_tables') 
    else:
        ware = warehouse.objects.all()
        return render(request, 'update_ware.html', {'ware': ware})  

def update_sup(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        phone = request.POST.get("phone")  # Updated phone number
        
        # Check if the customer exists
        data = supplier.objects.get(name=name)
        if data:
            # Update the phone number
            data.phone = phone
            data.save()  # Save the changes to the database
            messages.success(request, "Supplier details have been updated successfully")
        else:
            messages.error(request, "Supplier does not exist")
        
        return redirect('update_tables') 
    else:
        sup = supplier.objects.all()
        return render(request, 'update_sup.html', {'sup': sup})       
    
def update_shipment(request):
    if request.method == 'POST':
        routes_id = request.POST.get("routes_id")
        id = request.POST.get("id")
        departure_date = request.POST.get("departure_date")
        arrival_date = request.POST.get("arrival_date")
        
        ship_obj = shipment.objects.filter(routes_id=routes_id)
        ship_obj = shipment.objects.get(id=id)
        if ship_obj:
            ship_obj.routes_id = routes_id
            ship_obj.id = id
            ship_obj.departure_date = departure_date
            ship_obj.arrival_date = arrival_date
            ship_obj.save()
            messages.success(request, "Shipment details have been updated successfully")
        else:
            messages.error(request, "Shipment does not exist")
        return redirect('update_tables')  # Redirect to update_tables or wherever needed
    else:
        shipments = shipment.objects.all()
        return render(request, 'update_shipment.html', {'shipments': shipments})      

def route_map(request):
    routes = route.objects.all()
    return render(request, 'map.html',{'routes':routes})

def map(request):
    return render(request, 'route_map.html')

def view_sup(request):
    sup = supplier.objects.all()
    data={
       'sup':sup
    }  
    return render(request,'view_sup.html',data)

def view_route(request):
    routes = route.objects.all()
    data={
       'routes':routes
    }  
    return render(request,'view_route.html',data)

def view_ware(request):
    ware = warehouse.objects.all()
    data={
       'ware':ware
    }  
    return render(request,'view_ware.html',data)

def view_payments(request):
    ware = payment.objects.all()
    data={
       'ware':ware
    }  
    return render(request,'view_payments.html',data)

def view_package(request):
    ware = package.objects.all()
    data={
       'ware':ware
    }  
    return render(request,'view_package.html',data)

