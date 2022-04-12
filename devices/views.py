# import uuid
from cgitb import enable
from django.apps import apps
from django.core import serializers
from django.db import models

from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponse
from .forms import DeviceField
from .models import DeviceImages

from devices.forms import DeviceForm
from devices.models import Device



@login_required(login_url="/login/")
@csrf_exempt
def device_add(request):
    """
    :param request:
    :return:
    """
    device_add = True
    msg_ok = ""
    msg_err = ""

    # context = {'p':p}

    if request.method == 'POST':
        # enable = request.POST['enable',] == 'on'
        form = DeviceForm(request.POST)
        file_image = DeviceField(request.POST or None, request.FILES or None,)          
        files = request.FILES.getlist('device_images')
        if form.is_valid() and file_image.is_valid():
            device_name = form.cleaned_data.get('name')
            device_type = form.cleaned_data.get('device_type')
            device_id = form.cleaned_data.get('device_id')
            lane_1 = form.cleaned_data.get('lane_1')
            enable_1 = form.cleaned_data.get('enable_1')
            lane_2 = form.cleaned_data.get('lane_2')
            enable_2 = form.cleaned_data.get('enable_2')
            lane_3 = form.cleaned_data.get('lane_3')
            enable_3 = form.cleaned_data.get('enable_3')
            lane_4 = form.cleaned_data.get('lane_4')
            enable_4 = form.cleaned_data.get('enable_4')
            description= form.cleaned_data.get('description')
            state = form.cleaned_data.get('state')
            city = form.cleaned_data.get('city')
            latitude = form.cleaned_data.get('lat')
            longitude = form.cleaned_data.get('lng')
            enable = form.cleaned_data.get('enable')
            print(enable)
            device_save = Device.objects.create(name = device_name, device_type = device_type, device_id = device_id, 
            lane_1 = lane_1, enable_1 = enable_1, lane_2 = lane_2, enable_2 = enable_2, lane_3 = lane_3, enable_3 = enable_3, 
            lane_4 = lane_4, enable_4 = enable_4,  description = description, state = state, city = city, lat = latitude, lng = longitude, enable = enable)

            for file in files:
                DeviceImages.objects.create(feed=device_save, device_images=file)
            


            # form.save()

            # completed = request.POST.get('completed', '') == 'on'
            # if not completed:
            #   completed = False
            # toSave = models.Device(enable=enable)
            # models.myClass(completed=completed)
            # f = form.save(commit=False)
            # f.owner = request.user
            # f.api_key = (uuid.uuid4().hex)[:20] + (uuid.uuid4().hex)[:20]

            # x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            # if x_forwarded_for:
            #     f.remote_address = x_forwarded_for.split(',')[-1].strip()
            # else:
            #     f.remote_address = request.META.get('REMOTE_ADDR') + "&" + request.META.get(
            #         'HTTP_USER_AGENT') + "&" + request.META.get('SERVER_PROTOCOL')

            # f.save()
            msg_ok = _(u'Added device successfully')
        else:
            msg_err = _(u'Attention! Please correct the errors!')

    form = DeviceForm()

    return render(request, "home/device-add.html", locals())


@login_required(login_url="/login/")
def device_list(request):
    """
    :param request:
    :return:
    """
    device_list = True
    list = Device.objects.all()

    return render(request, "home/device-list.html", locals())


@login_required(login_url="/login/")
def device_edit(request, id):
    """
    :param request:
    :param id:
    :return:
    """
    val = get_object_or_404(Device, id=id)

    form = DeviceForm(request.POST or None, request.FILES or None, instance=val)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            msg_ok = _('Device updated successfully')
            return HttpResponseRedirect(reverse('device_list'))
        else:
            msg_err = _(u'Attention! Please correct the errors!')

    return render(request, "home/device-list.html", locals())


# @login_required(login_url="/login/")
# def device_delete(request, id=None):
#     """
#     :param request:
#     :param id:
#     :return:
#     """
#     device = get_object_or_404(Device, id=id).delete()

#     msg_ok = _(u'Device deleted')

#     return HttpResponseRedirect(reverse('device_list'), locals())

def delete_device(request, id):
    device = Device.objects.get(id=id)
    device.delete()
    return redirect('/device/list')




# @login_required(login_url="/login")
def change_state(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method=='POST':
        print(request)
        state = Device.objects.get(id=request.POST['id'])
        # print('state')
        state.enable = True if request.POST.get('enable') == 'true' else False
        print(state)
        state.save()
        data = {'status':'success', 'enable':state}
        return JsonResponse(data, status=200)
    else:
        data = {'status':'error'}
        return JsonResponse(data, status=400)
# def key_list(request):
#     """
#     :param request:
#     :return:
#     """
#     key_list = True
#     list = Device.objects.filter(enable=True)
#     return render(request, "back/key_list.html", locals())


# @login_required(login_url=LOGIN_URL)
# def generate_key(request, id=None):
#     """
#     :param request:
#     :param id:
#     :return:
#     """
#     val = get_object_or_404(Device, id=id)
#     val.api_key = val.generate_key()
#     val.save()
#     list = Device.objects.filter(enable=True)
#     msg_ok = _(u'Key Generated')

#     return HttpResponseRedirect(reverse('key_list'), locals())


def export(request, model):
    """
    :param request:
    :return:
    """
    model = apps.get_model(app_label=model + 's', model_name=model)

    data = serializers.serialize(request.GET['format'], model.objects.all()[:100])

    return JsonResponse({'response_data': data})

