from api.models import Person
import time
import base64
import struct

__author__ = 'hanson'
from random import choice
import string


def get_token(length=8, chars=string.ascii_letters + string.digits):
    return ''.join([choice(chars) for _ in range(length)])


def check_token(token, phone_number):
    if token is None and token == '':
        return False
    person = Person.objects.get(phone_number=phone_number)
    return person.token == token


def encode_token():
    return base64.encodestring(struct.pack('sd', b"c", time.time()))


def decode_check_token(s):
    return time.time() - struct.unpack('sd',base64.decodestring(s))[1]  < 600.0
