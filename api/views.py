# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Person, Message, Comment, SystemMsg, News, CampusAmbassador
from api.serializers import PersonSerializer, MessageSerializer, CommentSerializer, WordsSerializer, \
    NewsSerializer, SystemMsgSerializer, FeedbackSerializer, CampusAmbassadorSerializer
from api.util.check_authentication import MobSMS
from api.util.token_helper import check_token, get_token, encode_token, decode_check_token
import hashlib


@api_view(['GET'])
def check_person_exist(request):
    try:
        Person.objects.get(phone_number=request.GET.get('phone_number', ''))
    except Person.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def verify_phone(request):
    if MobSMS().verify_sms_code("86", request.GET["phone_number"], request.GET["identify"]):
        return Response(encode_token())
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def regist_member(request):
    if not decode_check_token(request.POST['identify']):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    serializer = PersonSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(password=hashlib.md5(request.POST["password"]).hexdigest())
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_201_CREATED)


@api_view(['POST'])
def logout_member(request):
    phone_number = request.POST["phone_number"]
    if not check_token(request.POST["token"], phone_number):
        return Response(data={'detail': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    obj = Person.objects.get(phone_number=phone_number)
    obj.token = ""
    obj.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_member(request):
    try:
        obj = Person.objects.get(phone_number=request.GET.get('phone_number', ''))
    except Person.DoesNotExist:
        return Response(data={'detail': 'person does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    person = PersonSerializer(obj)
    data = person.data.copy()
    del data['token']
    del data['password']
    return Response(data=data)


@api_view(['GET'])
def get_commited(request):
    try:
        obj = Person.objects.get(phone_number=request.GET.get('phone_number', ''))
    except Person.DoesNotExist:
        return Response(data={'detail': 'person does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    msg_ser = MessageSerializer(obj.messages, many=True)
    news_ser = NewsSerializer(obj.news, many=True)
    return Response({"messages": msg_ser.data, "news": news_ser.data})


@api_view(['POST'])
def patch_member(request):
    phone_number = request.POST.get("phone_number", "")
    try:
        person = Person.objects.get(phone_number=phone_number)
    except Person.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    operation = request.POST.get("operation", "")
    if operation == 'change_password':
        mobsms = MobSMS()
        if not mobsms.verify_sms_code("86", request.POST["phone_number"], request.POST["identify"]):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        person.password = hashlib.md5(request.POST["password"]).hexdigest()
    elif operation == 'change_portrait':
        if not check_token(request.POST.get("token", ''), phone_number):
            return Response(data={'detail': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        person.portrait = request.FILES['portrait']
    elif operation == 'change_others':
        if not check_token(request.POST.get("token", ''), phone_number):
            return Response(data={'detail': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        person.name = request.POST['name']
        person.location = request.POST['location']
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    person.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def login_member(request):
    try:
        the_object = Person.objects.get(phone_number=request.POST["phone_number"])
    except Person.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    password = hashlib.md5(request.POST["password"]).hexdigest()
    if the_object.password == password:
        the_object.token = get_token()
        the_object.save()
        return Response({'token': the_object.token})
    else:
        return Response(data={'detail': "wrong password"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def operate_message(request):
    phone_number = request.POST.get("phone_number", '')
    if not check_token(request.POST.get("token", ''), phone_number):
        return Response(data={'detail': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    id_ = request.POST.get('id', '')
    operation = request.POST.get('operation', '')
    try:
        message = Message.objects.get(id=id_)
    except Message.DoesNotExist:
        return Response(data={'detail': 'message does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    if operation == 'DELETE':
        if message.commit_person_id == phone_number:
            for comment in message.comment_set.iterator():
                comment.delete()
            message.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(data="this message's owner is not you", status=status.HTTP_400_BAD_REQUEST)
    elif operation == 'COMMENT':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(commit_person_id=phone_number, message=message)
            message.comments_number += 1
            message.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif operation == 'UNCOMMENT':
        serializer = Comment.objects.get(id=request.POST['comment_id'])
        if serializer.commit_person_id == phone_number:
            serializer.delete()
            message.comments_number -= 1
            message.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status.HTTP_401_UNAUTHORIZED)
    elif operation == 'SHARE':
        message.share_number += 1
        message.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def add_message(request):
    phone_number = request.POST.get("phone_number", '')
    if not check_token(request.POST.get("token", ""), phone_number):
        return Response(data={'detail': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    serializer = MessageSerializer(data=request.data)
    if serializer.is_valid():
        person = Person.objects.get(phone_number=phone_number)
        serializer.save(commit_person_id=phone_number, commit_location=person.location)
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_messages(request):
    location = request.GET['location']
    start = request.GET['start']
    end = request.GET['end']
    what = request.GET['what']
    kind = request.GET['kind']
    all_locations = (location == u'全国')
    all_kind = (kind == u'所有')
    if all_locations and all_kind:
        messages = Message.objects.filter(what=what).order_by('-created')[int(start):int(end)]
    elif not all_locations and all_kind:
        messages = Message.objects.filter(what=what, commit_location=location).order_by('-created')[int(start):int(end)]
    elif not all_locations and not all_kind:
        messages = Message.objects.filter(what=what, commit_location=location, kind=kind).order_by('-created')[
                   int(start):int(end)]
    else:
        messages = Message.objects.filter(what=what, kind=kind).order_by('-created')[int(start):int(end)]

    ser = MessageSerializer(messages, many=True)
    return Response(ser.data)


@api_view(['GET'])
def get_one_message(request):
    _id = request.GET['id']
    msg = Message.objects.get(id=_id)
    ser = MessageSerializer(msg)
    return Response(ser.data)


@api_view(['GET'])
def get_comments(request):
    if request.GET['kind'] == 'message':
        msg = Message.objects.get(id=request.GET['id'])
    else:
        msg = News.objects.get(id=request.GET['id'])
    msg.reading_number += 1
    msg.save()
    comments = msg.comment_set
    ser = CommentSerializer(comments, many=True)
    return Response(ser.data)


@api_view(['POST'])
def add_news(request):
    phone_number = request.POST["phone_number"]
    if not check_token(request.POST["token"], phone_number):
        return Response(data={'detail': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    serializer = NewsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(commit_person_id=phone_number)
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def operate_news(request):
    phone_number = request.POST["phone_number"]
    if not check_token(request.POST["token"], phone_number):
        return Response(data={'detail': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    id_ = request.POST.get('id', '')
    operation = request.POST.get('operation', '')
    try:
        news = News.objects.get(id=id_)
    except News.DoesNotExist:
        return Response(data={'detail': 'news does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    if operation == 'DELETE':
        if news.commit_person_id == phone_number:
            for comment in news.comment_set.iterator():
                comment.delete()
            news.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(data="this message's owner is not you", status=status.HTTP_401_UNAUTHORIZED)
    elif operation == 'COMMENT':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(commit_person_id=phone_number, news=news)
            news.comments_number += 1
            news.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif operation == 'UNCOMMENT':
        comment = Comment.objects.get(id=request.POST['comment_id'])
        if comment.commit_person_id == phone_number:
            comment.delete()
            news.comments_number -= 1
            news.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status.HTTP_401_UNAUTHORIZED)
    elif operation == 'FOLLOW':
        person = Person.objects.get(phone_number=phone_number)
        news.followers.add(person)
        news.following_number += 1
        news.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif operation == 'UNFOLLOW':
        person = Person.objects.get(phone_number=phone_number)
        news.followers.remove(person)
        news.following_number -= 1
        news.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif operation == 'SHARE':
        news.share_number += 1
        news.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_news(request):
    start = request.GET['start']
    end = request.GET['end']
    news = News.objects.all().order_by('-created')[int(start):int(end)]
    ser = NewsSerializer(news, many=True)
    return Response(ser.data)


@api_view(['GET'])
def get_one_news(request):
    _id = request.GET['id']
    news = News.objects.get(id=_id)
    ser = NewsSerializer(news)
    return Response(ser.data)


@api_view(['POST'])
def add_words(request):
    phone_number = request.POST["phone_number"]
    if not check_token(request.POST["token"], phone_number):
        return Response(data={'detail': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    ser = WordsSerializer(data=request.data)
    from_person = Person.objects.get(phone_number=phone_number)
    to_person = Person.objects.get(phone_number=request.POST['to_phone_number'])
    if ser.is_valid():
        ser.save(from_person=from_person, to_person=to_person)
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def delete_words(request):
    phone_number = request.POST["phone_number"]
    if not check_token(request.POST["token"], phone_number):
        return Response(data={'detail': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    to_number = request.POST["to_phone_number"]
    from_number = request.POST["from_phone_number"]
    _id = request.POST["id"]
    if not phone_number == from_number and not phone_number == to_number:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    words = Person.objects.get(phone_number=to_number).words.get(from_person=from_number).get(id=_id)
    words.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def get_words(request):
    phone_number = request.POST["phone_number"]
    if not check_token(request.POST["token"], phone_number):
        return Response(data={'detail': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    number = request.POST['to_phone_number']
    start = request.POST.get('start', '')
    end = request.POST.get('end', '')

    if not start == '' and not end == '':
        data = Person.objects.get(phone_number=number).words.order_by("-created")[int(start):int(end)]
    else:
        data = Person.objects.get(phone_number=number).words.order_by("-created")[int(start):]

    def _change(obj):
        obj.if_read = True
        obj.save()

    try:
        ser = WordsSerializer(data, many=True)
        return Response(ser.data)
    finally:
        if number == phone_number:
            map(_change, data)


@api_view(['POST'])
def get_replies(request):
    phone_number = request.POST["phone_number"]
    if not check_token(request.POST["token"], phone_number):
        return Response(data={'detail': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    time = request.POST['time']
    replies = Person.objects.get(phone_number=phone_number).replies.extra(where=["created > %s"], params=[time])
    ser = CommentSerializer(replies, many=True)
    return Response(ser.data)


@api_view(['GET'])
def get_system_msg(request):
    time = request.GET['time']
    msgs = SystemMsg.objects.extra(where=["created > %s"], params=[time])
    ser = SystemMsgSerializer(msgs, many=True)
    return Response(data=ser.data)


@api_view(['GET'])
def get_update(request):
    version = request.GET['version']
    with open('../static/release/version_number', 'r') as version_file:
        version_now = version_file.read()
        if version >= version_now:
            return Response(status=status.HTTP_204_NO_CONTENT)
    with open('../static/release/update/information', 'r') as info_file:
        dic = {'content': info_file.read(), 'url': 'http://123.56.150.30:8000/static/release/update/YiDiudiu.apk',
               'version': version_now}
        return Response(data=dic)


@api_view(['POST'])
def feedback(request):
    ser = FeedbackSerializer(data=request.data)
    if ser.is_valid():
        ser.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(data=ser.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_ambassadors(request):
    objs = CampusAmbassador.objects.all()
    ser = CampusAmbassadorSerializer(objs, many=True)
    return Response(ser.data)
