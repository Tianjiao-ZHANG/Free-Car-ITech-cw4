from django.shortcuts import get_object_or_404, render
from django.core import serializers
from django.http import HttpResponse, response
import json, random, time
from .models import user, bike
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
def get_session_key(max:int):
    timestamp = str(int(time.time()))
    for i in range(max):
        timestamp = timestamp + str(random.randint(0, 10))

    return timestamp

@api_view(['POST'])
def signup(request):
    username = request.POST.get('username')
    password = request.POST.get('pass')
    mail = request.POST.get('mail')
    balance = 0

    try:
        user_flag=user(username=username,password=password,mail=mail,balance=balance,status=False)
        get_object_or_404(user, username=username)

        response = HttpResponse()
        response.status_code = 900
        return response
    except:
        user_flag.save()
        user_record=user.objects.all().filter(username=username)
        user_record_json = serializers.serialize('json',user_record)

        return HttpResponse(user_record_json, content_type='application/json')
    
@api_view(['POST'])
def login(request):
    username = request.POST.get('username')
    password = request.POST.get('pass')

    data = {}
    try:
        user_already = get_object_or_404(user, username=username)
        
        data['username'] = user_already.__getattribute__('username')
        if user_already.__getattribute__('password')==password:
            user_already.status=True
            user_already.save()

            request.session['session_key']=get_session_key(32)
            request.session['balance']=user_already.__getattribute__('balance')
            # request.session.set_expiry(0)
            
            data['session_key']=request.session['session_key']
            data['balance']=user_already.__getattribute__('balance')

            return HttpResponse(json.dumps(data))
        else:
            response = HttpResponse(username)
            response.status_code = 900
            return response
    except:
        response = HttpResponse()
        response.status_code = 901
        return response

@api_view(('POST',))
def logout(request):
    username = request.POST.get("username")
    try:
        user_flag = get_object_or_404(user, username=username)
        user_flag.status=False
        user_flag.save()

        request.session.delete(request.session.session_key)
        request.session.flush()

        return HttpResponse(True)
    except:
        response = HttpResponse()
        response.status_code=404
        return response

@api_view(('POST',))
def rent(request):
    cost = float(request.POST.get('cost'))
    username = (request.POST.get('username'))
    pk = (request.POST.get('pk'))
    user_already = get_object_or_404(user, username=username)
    if (user_already.balance-cost)>0:
        user_already.balance=user_already.balance-cost
        user_already.save()
        bike_already = get_object_or_404(bike, pk=pk)
        bike_already.avaliable = False
        bike_already.save()
    
        response = HttpResponse(user_already.balance)
    else:
        response = HttpResponse(user_already.balance)
        response.status_code=404

    return response

@api_view(('POST',))
def rent_back(request):
    pk = request.POST.get('pk')
    bike_already = get_object_or_404(bike, pk=pk)
    bike_already.avaliable = True
    bike_already.save()

    return HttpResponse(bike_already.avaliable)

@api_view(('POST',))
def add_balance(request):
    money=float(request.POST.get('money'))
    username = request.POST.get('username')
    user_flag=get_object_or_404(user, username=username)

    user_flag.balance+=money
    user_flag.save()

    return HttpResponse(user_flag.balance)


@api_view(('GET',))
def get_bikes(request):
    data=bike.objects.filter(avaliable=True)
    data_json = serializers.serialize('json', data)
    return HttpResponse(data_json)

@api_view(('POST',))
def population_script(request):
    num=int(request.POST.get('iter'))

    brand=['giant','anta','jumped-up','rowling']

    for idx in range(num):
        bike.objects.create(iid=10000,
                            brand=brand[random.randint(0,3)],
                            avaliable=True,
                            price=random.randint(5,10))

    return HttpResponse('ok')