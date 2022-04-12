
from django import template
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.auth import get_user_model, logout
from .consumers import NotificationConsumer

from devices.models import Device

from .permissions import IsAdminUser, AdvancedUserManage

from .serializers import DeviceSerializer, LoginSerializer, RegistrationSerializer, UsersSerializer

from .models import NotificationChannel, UserDetailsFile, UserDevices, UserProfile

from .forms import CreateUserDevice, CreateUsers, LoginForm, ProfileForm, SignUpForm, User, UserDeviceImage
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response



# Create your views here.
# User = get_user_model()
def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        context ={
            "form" : form
        }
        if form.is_valid():
            print('check')
            form.save()
                     
            return redirect("/login")
        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            print(f'User is: {user}')
            print(f'username is: {email}')
            print(f'password is: {password}')
            print(user)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def logout_view(request):
    logout(request)
    return redirect("/login")


# After successfull login user is taken to homepage
# @login_required(login_url= "/login/")
def home(request):
    msg = "Not authenticated "
    if request.user.is_authenticated:
        # get all users using the system

        all_users = get_user_model().objects.all().filter(admin__in = [True]).count()
        all_devices = Device.objects.all().count()
        normal_users = get_user_model().objects.all().filter(normal_user__in = [True]).count()
        advanced_users = get_user_model().objects.filter(advanced_user__in = [True]).count()
        active_users = get_user_model().objects.filter(is_active__in = [True]).count()
        notifications = NotificationChannel.objects.all().filter(user_id = request.user.id).count()

        print(notifications)

        if request.user.staff:
           user_devices = UserDevices.objects.all()
           devices_count = user_devices.count()
        else:
            user_devices = UserDevices.objects.filter(user_detail_id=request.user.id)
            devices_count = user_devices.count()
            print(f'user devices count is: {devices_count}')

        

        # 'allusers' = all_users, 'alldevices': all_devices, 'normalusers':normal_users, 'advancedusers': advanced_users , 'activeusers': active_users, 'userdevices': user_devices, 'devicescount': devices_count
        return render(request, "home/index.html", {'room': 'broadcast', 'allusers': all_users, 'alldevices': all_devices, 'normalusers':normal_users, 'advancedusers': advanced_users , 'activeusers': active_users, 'userdevices': user_devices, 'devicescount': devices_count, 'notification_count': notifications})
    return render(request, "accounts/login.html") 


@login_required(login_url="/login/")
def notifications_view(request):
    user_notifications = NotificationChannel.objects.all().filter(user_id = request.user.id)
    notifications = NotificationChannel.objects.all().filter(user_id = request.user.id).count()
    return render(request, "home/notifications.html",{'user_notifications': user_notifications, 'notification_count': notifications})


@login_required(login_url="/login/")
def create_users(request):
    msg = None
    success = False
    
    if request.method == "POST":
        form = CreateUsers(request.POST)
        context ={
            "form" : form
        }
        # context['form']= form
        if form.is_valid():
            
            form.save()

            msg = "User is created"
            return redirect('/users/list/')
        else:
            msg = 'Form is not valid'
            print(msg)
    else:
        form = CreateUsers()
    
    return render(request, "home/users-add.html", {"form": form, "msg": msg, "success": success})  
    
    
 
@login_required(login_url="/login/")
def users_list(request):
    """
    :param request:
    :return:
    """
    users_list = True
    list = User.objects.all()
    return render(request, "home/users-list.html", locals())

@login_required(login_url="/login/")
def delete_user(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect('/users/list')

# Profile management
@login_required(login_url="/login/")
def profile_add(request):
    msg = None
    success = False
    profile = UserProfile.objects.create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST,  request.FILES, instance=request.user.profile)
        if form.is_valid():
            username = form.cleaned_data.get("user_name")
            address = form.cleaned_data.get("address")
            country = form.cleaned_data.get("country")
            state = form.cleaned_data.get("state")
            zip = form.cleaned_data.get("zip")
            city = form.cleaned_data.get("city")
            about = form.cleaned_data.get("about")
            photo = form.cleaned_data.get("photo")
            print(photo)
            fullname = User.objects.get('full_name')
            
            # user.full_name = fullname
            # user.address = address
            # user.country = country
            profiler = UserProfile(full_name=fullname, user_name=username, address=address, country=country, state=state, zip=zip, city=city, about=about, photo=photo)
            
            profiler.save()
            msg = 'Added device successfully'
        else:
            msg = 'Form is not valid'
    else:
        form = ProfileForm(initial={'user_name': request.user.profile.user_name, 'address': request.user.address, 'country': request.user.country, 'state': profile.state, 'zip': profile.zip, 'city': profile.city, 'about': profile.about})
        print(form)
    # usersdatas = UserProfile.objects.get(full_name=request.user) 
    context ={"form" : form, "msg": msg, "success": success}   
    return render(request, "home/profile.html",  context)

@login_required(login_url="/login/")
def users_device_add(request):
    msg = None
    success = False
    context_dict={}
    
    if request.method == "POST":
        form = CreateUserDevice(request.POST, instance=request.user)
        file_image = UserDeviceImage(request.POST or None,request.FILES or None, )    
        files = request.FILES.getlist('device_images')
              
        if form.is_valid() or file_image.is_valid:
            
   
            device_name = Device.objects.get(name=form.cleaned_data.get("device_name"))
            device_type = form.cleaned_data.get("device_type")
            lane_1 = form.cleaned_data.get("lane1")
            lane_2 = form.cleaned_data.get("lane2")
            lane_3 = form.cleaned_data.get("lane3")
            lane_4 = form.cleaned_data.get("lane4")
            status = form.cleaned_data.get("example-inline-radios")
            print(status)

            device_status = form.cleaned_data.get("device_status")
            state = form.cleaned_data.get("state")
            city = form.cleaned_data.get("city")
            latitude = form.cleaned_data.get("lng")
            longitude = form.cleaned_data.get("lat")
            userdev = UserDevices.objects.create(user_detail= request.user, device_name=device_name, device_type=device_type,lane1=lane_1, lane2=lane_2, lane3=lane_3, lane4=lane_4, device_status=device_status, state=state, city=city, lat=latitude, lng=longitude)
            for f in files:
                UserDetailsFile.objects.create(feed=userdev, device_images=f)
                
            return redirect('/home')
        else:
            msg = 'Error validating the form'
            print(msg)
    else:
        form =  CreateUserDevice()
        file_image = UserDeviceImage()
        if request.user.normal_user:
            devices = Device.objects.order_by('id')[:2]
            users = User.objects.filter(id = request.user.id)
            print(users)
        elif request.user.advanced_user:
            devices = Device.objects.all()
            users = User.objects.filter(id = request.user.id)
        else:
            devices = Device.objects.all()
            users = User.objects.all()
        
        # context_dict = {'form': form, 'devices': devices, 'users': users, 'msg': msg, 'success': success}
        context_dict['form'] = form
        context_dict['devices'] = devices
        context_dict['users'] = users
       
    return render(request, "home/user-devices.html", context_dict)



@login_required(login_url="/login/")
def users_device_list(request):
    """
    :param request:
    :return:
    """
    users_list = True
    list = UserDevices.objects.all()
    return render(request, "home/users-device-list.html", locals())



@login_required(login_url="/login/")
def user_device_delete(request, id):
    user_device = UserDevices.objects.get(id=id)
    user_device.delete()
    return redirect('/users/list')    

@login_required(login_url="/login/")
def profile(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))



@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

# APIViews
class CurrentUserViewSet(APIView):
    permission_class = (IsAuthenticated)
    queryset = User.objects.all()
    serializer_class = UsersSerializer

def UserAvailable(request):
    if request.method == 'GET':
        specific_users = User.objects.filter(id=request.user.id)
        serializer = UsersSerializer(specific_users)
        return Response(serializer.data)



class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = [IsAdminUser]
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # The `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class DeviceAPIView(APIView):
    permission_class = (IsAuthenticated)
    serializer_class = DeviceSerializer

    def get(self, request):
        user = request.user
        if user.staff or user.advanced_user:
            devices = Device.objects.all()
            serializer = self.serializer_class(devices, many=True)

            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched devices',
                'devices': serializer.data

            }
            return Response(response, status=status.HTTP_200_OK)

        else:
            devices = Device.objects.order_by('id')[:10]
            serializer = self.serializer_class(devices, many=True)

            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched devices',
                'devices': serializer.data

            }
            return Response(response, status=status.HTTP_200_OK)
        


    

