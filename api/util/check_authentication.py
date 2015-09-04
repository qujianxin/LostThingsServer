import requests

__author__ = 'hanson'


class MobSMS:
    def __init__(self):
        self.appkey = '5aec12823819'
        self.verify_url = 'https://api.sms.mob.com:8443/sms/verify'

    def verify_sms_code(self, zone, phone, code):
        data = {'appkey': self.appkey, 'phone': phone, 'zone': zone, 'code': code}
        req = requests.post(self.verify_url, data=data, verify=False)
        return req.status_code == 200