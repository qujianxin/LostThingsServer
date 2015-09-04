# coding=utf-8
import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from api.models import Person, OpenAppRecord, RecordWatcher

__author__ = 'hason'

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def record_openapp(request):
    day = datetime.date.today()
    today = str(day.year) + '-' + str(day.month) + '-' + str(day.day)
    try:
        obj = OpenAppRecord.objects.get(date=today)
    except OpenAppRecord.DoesNotExist:
        obj = OpenAppRecord.objects.create()
    if 'phone_number' in request.GET.keys():
        phone_number = request.GET['phone_number']
        try:
            person = Person.objects.get(phone_number=phone_number)
        except Person.DoesNotExist:
            return Response()
        obj.people.add(person)
        obj.regist_times += 1
    obj.times += 1
    obj.save()
    return Response()


def login_statistcs(request):
    if request.method == 'POST':
        name = request.POST['name']
        password = request.POST['password']
        watcher = RecordWatcher.objects.filter(name__exact=name)
        if watcher:
            person = watcher.first()
            if person.password == password:
                request.session['name'] = name
                response = HttpResponseRedirect('/statistics/index.html')
            else:
                response = render_to_response('login.html', {'name': name, 'wrong_password': True})
        else:
            response = render_to_response('login.html', {'name': name, 'user_not_exist': True})
    else:
        response = render_to_response('login.html')

    return response


def index_statistcs(request):
    name = request.session.get('name', '')
    number = 20
    watcher = RecordWatcher.objects.filter(name__exact=name)
    if watcher:
        today = datetime.date.today()
        days = []
        for i in range(number):
            days.append(today + datetime.timedelta(-i))
        all_records = []
        regist_records = []
        user_records = []
        records = OpenAppRecord.objects.extra(where=["date > %s"], params=[today + datetime.timedelta(-number)])
        for i in range(number):
            var = len(Person.objects.extra(where=["created = %s"], params=[today + datetime.timedelta(-i)]))
            user_records.append(var)
        for record in records:
            all_records.append(record.times)
            regist_records.append(record.regist_times)
        if len(records) < number:
            for i in range(number - len(records)):
                all_records.append(0)
                regist_records.append(0)
        return render_to_response('index.html',
                                  {"name": name, "all_records": all_records, 'regist_records': regist_records,
                                   'user_records': user_records,
                                   'days': days})
    else:
        return HttpResponseRedirect('/statistics/login')


def logout_statistcs(request):
    del request.session['name']
    return HttpResponseRedirect('/statistics/login')
