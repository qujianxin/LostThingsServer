# -*- coding: UTF-8 -*-

from django.template.loader import get_template
from django.http import HttpResponse
from django.template import Context
from api.models import Message, News
from rest_framework.response import Response
from rest_framework import status


def image_list(id_):
    msg = Message.objects.get(id=id_)
    l = []
    for image in msg.image1, msg.image2, msg.image3:
        try:
            url = image.url
        except ValueError:
            continue
        l.append(url)
    return l


def comment_list(id_):
    msg = Message.objects.get(id=id_)
    c = msg.comment_set.all()[0:3]
    return c


def comment_list_else(id_):
    msg = Message.objects.get(id=id_)
    c = msg.comment_set.all()
    l = len(list(c))
    if l >= 3:
        f = c[3:]
        return f


def hello_html(request, id_):
    try:
        msg = Message.objects.get(id=id_)
    except Message.DoesNotExist:
        return Response(data={'detail': "message does not exits"}, status=status.HTTP_404_NOT_FOUND)
    msg.reading_number += 1
    msg.save()
    t = get_template('new02.html')
    html = t.render(Context({'commit_person': msg.commit_person,
                             'portrait': msg.commit_person.portrait.url,
                             'created': msg.created,
                             'what': msg.what,
                             'kind': msg.kind,
                             'title': msg.title,
                             'time': msg.time,
                             'commit_person_location': msg.commit_person.location,
                             'location': msg.location,
                             'information': msg.information,
                             'contact_phone': msg.contact_phone,
                             'comments_number': msg.comments_number,
                             'reading': msg.reading_number,
                             'image_list': image_list(id_),
                             'comments': comment_list(id_),
                             'comments_else': comment_list_else(id_),
                             }))
    return HttpResponse(html)


def image_list1(id_):
    msg = News.objects.get(id=id_)
    l = []
    for image in msg.image1, msg.image2, msg.image3:
        try:
            url = image.url
        except ValueError:
            continue
        l.append(url)
    return l


def comment_list1(id_):
    msg = News.objects.get(id=id_)
    c = msg.comment_set.all()[0:3]
    return c


def comment_list_else1(id_):
    msg = News.objects.get(id=id_)
    c = msg.comment_set.all()
    l = len(list(c))
    if l >= 3:
        f = c[3:]
        return f


def news_html(request, id_):
    try:
        msg = News.objects.get(id=id_)
    except Message.DoesNotExist:
        return Response(data={'detail': "message does not exits"}, status=status.HTTP_404_NOT_FOUND)
    t = get_template('new02.html')
    html = t.render(Context({'commit_person': msg.commit_person,
                             'portrait': msg.commit_person.portrait.url,
                             'created': msg.created,
                             # 'what': msg.what,
                             # 'kind': msg.kind,
                             'title': msg.title,
                             # 'time': msg.time,
                             'commit_person_location': msg.commit_person.location,
                             # 'location': msg.location,
                             'information': msg.information,
                             # 'contact_phone': msg.contact_phone,
                             'comments_number': msg.comments_number,
                             'reading': msg.reading_number,
                             'image_list': image_list1(id_),
                             'comments': comment_list1(id_),
                             'comments_else': comment_list_else1(id_),
                             }))
    return HttpResponse(html)
