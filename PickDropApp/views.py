from django.shortcuts import render,redirect
from PickDropApp.models import *
from geopy.geocoders import Nominatim
 
from geopy.distance import geodesic
from django.http import JsonResponse
# Create your views here.

def home(request):
    
    return render(request, 'home.html')


def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        mobile = request.POST.get('mobile')

        try:
            user_registration_model.objects.create(
                username = username,
                email = email,
                password = password,
                mobile = mobile,
            )
            
        except Exception as e: 
            print(e)
    return render(request, 'user_registration.html')

def professional_registration(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        mobile = request.POST.get('mobile')
        specialization = request.POST.get('specialization')
        drone_type = request.POST.get('drone_type')
        load_capacity = request.POST.get('load_capacity')
        location = request.POST.get('location')

        try:
            professional_registration_model.objects.create(
                name = name,
                email = email,
                password = password,
                mobile = mobile,
                specialization = specialization,
                drone_type = drone_type,
                load_capacity = load_capacity,
                location = location,
            )
            
        except Exception as e:
            print(e)
    return render(request,'pro_registration.html')

def login(request):
    if request.method == 'POST':
        email_id = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = user_registration_model.objects.get(email = email_id,password = password)
            

            # sotre user deatils in session 
            request.session['user_name'] = user.username
            request.session['user_email'] = user.email
            request.session['user_mobile'] = user.mobile

            return redirect('/user_dashboard')
        except user_registration_model.DoesNotExist:
            data = {'error':'invalid email','email':email_id}
            return redirect('/login',data)

        
    return render(request, 'login.html')

def professional_login(request):
    if request.method == 'POST':
        email_id = request.POST.get('email')
        password = request.POST.get('password')

        try:
            professional = professional_registration_model.objects.get(email = email_id, password = password)
            # store the details in the session
            # pendint this task 

            return redirect('/pro_dashboard')
        except user_registration_model.DoesNotExist:
            data = {'error':'invalid email','email':email_id}
            return redirect('/pro_login',data)
    return render(request,'pro_login.html')

# View for real-time suggestions
def get_suggestions(request):
    field = request.GET.get('field')
    query = request.GET.get('query')
    geolocator = Nominatim(user_agent="geoapiExercises")
    suggestions = []

    if query:
        try:
            locations = geolocator.geocode(query, exactly_one=False, limit=5)
            if locations:
                suggestions = [location.address for location in locations]
        except Exception as e:
            print(f"Error fetching suggestions: {e}")

    return JsonResponse({'suggestions': suggestions})

def user_dashboard(request):
    

    if request.method == 'POST':
        pickup = request.POST.get('pickup')
        dropoff = request.POST.get('dropoff')
        weight = request.POST.get('weight')

       
        try: 
            
            # use nominatim for geocoding the address
            geolocator = Nominatim(user_agent= "PickDropParcelApp")

            # get lat and long pickup 
            pickup_location = geolocator.geocode(pickup)
            if pickup_location is None:
                return JsonResponse({'error':'pickup location not found '}, status=400)
            
            pickup_coords = (pickup_location.latitude, pickup_location.longitude)

            # get lat and long dropoff
            dropoff_location = geolocator.geocode(dropoff)
            if dropoff_location is None:
                return JsonResponse({'error':'dropoff location not found '}, status=400)
            
            dropoff_coords = (dropoff_location.latitude, dropoff_location.longitude)

            # store in the DB
            user_dashboard_model.objects.create(
                pickup = pickup,
                dropoff = dropoff,
                weight = weight,
                user_email = request.session['user_email'],
                user_mobile = request.session['user_mobile'],
                pickup_latitude=pickup_coords[0],
                pickup_longitude=pickup_coords[1],
                dropoff_latitude=dropoff_coords[0],
                dropoff_longitude=dropoff_coords[1],
            )
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)
            
    # get the data from the database
    user_email = request.session.get('user_email')
    queryset = user_dashboard_model.objects.filter(user_email = user_email)


    user_name = request.session.get('user_name')
    # user_email = request.session.get('user_email')
    user_mobile = request.session.get('user_mobile')
    # queryset_m = user_registration_model.objects.get(user_mobile = user_mobile)

    # coordinates 
    if queryset:
        first_order = queryset.first()
        pickup_point = {
            'latitude': first_order.pickup_latitude,
            'longitude': first_order.pickup_longitude
        }
        dropoff_point = {
            'latitude':first_order.dropoff_latitude,
            'longitude': first_order.dropoff_longitude
        }
    else:
        pickup_point = {'latitude':0,'longitude':0}
        dropoff_point = {'latitude':0,'longitude':0}

    context = {
        'user_name': user_name,
        'user_email': user_email,
        'data_view':queryset,
        'pickup_point':pickup_point,
        'dropoff_point':dropoff_point,
        'user_mobile': user_mobile
        # 'distance': distance,
        # 'suggesstion_pickup': suggesstion_pickup,
        # 'suggesstion_dropoff': suggesstion_dropoff
    }
    
    return render(request,'user_dashboard.html',context)

def demo_page(request):
    return render(request, 'first_page.html')

def professional_dashboard(request):

    # if request.method == 'POST':
    #     accept = request.POST.get('accept') == 'true'
    #     reject = request.POST.get('reject') == 'true'
    #     try:
    #         professional_dashboard_model.objects.create(
    #             accept= accept,
    #             reject = reject
    #         )
    #     except Exception as e:
    #         print(e)

    # get the data from sessions
    pickup = request.session.get('pickup')
    dropoff = request.session.get('dropoff')
    weight = request.session.get('weight')
    queryset = user_dashboard_model.objects.all()
    context = {
        'pickup':pickup,
        'dropoff':dropoff,
        'weight':weight,
        'data_view':queryset
    }

    return render(request, 'pro_dashboard.html',context)

def order_reject(request, id):
    try:
        queryset = user_dashboard_model.objects.get(id = id)
        queryset.delete()
        return redirect('/pro_dashboard/')
    except user_dashboard_model.DoesNotExist:
        return JsonResponse({'error':'Order Not FFound'},status=400)
    
def order_accept(request,id,):
    # try:
    #     pickup_latitude = request.session.get('pickup_latitude')
    #     pickup_longitude = request.session.get('pickup_longitude')
    #     dropoff_latitude = request.session.get('dropoff_latitude')
    #     dropoff_longitude = request.session.get('dropoff_longitude')

    #     queryset = user_dashboard_model.objects.all()
    #     context = {
    #         'pickup_latitude': pickup_latitude,
    #         'pickup_longitude': pickup_longitude,
    #         'dropoff_latitude': dropoff_latitude,
    #         'dropoff_longitude': dropoff_longitude,
    #         'order': queryset
    #     }
    #     return render(request, '/order_accept/',context)
    # except user_dashboard_model.DoesNotExist:
    #     return JsonResponse({'error':'Order Not FFound'},status=400)
    
    # return render (request,'order_accept.html')
    try:
        order = user_dashboard_model.objects.get(id = id)
        user = user_registration_model.objects.get(email=order.user_email)
        user_mobile = request.session.get('mobile')
        context   = {
            'order': order,
            'user':user,
            'user_mobile':user_mobile     
        }
        
        return render(request, 'order_accept.html',context)
    except user_dashboard_model.DoesNotExist:
        return JsonResponse({'error':'Order Not Found'},status=400)


def order_nevigate(request,id):
    try:
        order = user_dashboard_model.objects.get(id = id)
        context = {
            'order':order
        }
        return render(request,'fly.html',context)
    except user_dashboard_model.DoesNotExist:
        return JsonResponse({'error':'Order Not Found'},status=400)

def get_coordinates(request,id):
    try:
        order = user_dashboard_model.objects.get(id=id)
        data ={
            'pickup_latitude': order.pickup_latitude,
            'pickup_longitude': order.pickup_longitude,
            'dropoff_latitude': order.dropoff_latitude,
            'dropoff_longitude': order.dropoff_longitude,
        }
        return JsonResponse(data)
    except user_dashboard_model.DoesNotExist:
        return JsonResponse({'error':'Order Not Found'},status=400)