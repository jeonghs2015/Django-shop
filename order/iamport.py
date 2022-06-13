from os import access
import requests
from django.conf import settings

# settings.py에 있는 API key, Secret key 를 가지고 IAMport에 가서 로그인 해주는 기능
def get_token():
    access_data = {
        'imp_key':settings.IAMPORT_KEY,
        'imp_secret':settings.IAMPORT_SECRET
    }
    url = "https://api.iamport.kr/users/getToken"
    # 크롤링 할때 사용하는 requests
    req = requests.post(url, data=access_data)
    # 크롤링할때는 보통 html 형태로 받아오지만 우리는 지금 api를 사용하기때문에 json 형태로 받아오게됨.
    access_res = req.json()

    if access_res['code'] is 0:
        return access_res['response']['access_token']
    else:
        return None


# 어떤 order_id로 얼마의 금액으로 결제를 요청할 건지 IAMport에 등록해주는 함수.
def payments_prepare(order_id, amount, *args, **kwargs):
    access_token = get_token()
    if access_token:
        access_data = {
            'merchant_uid':order_id,
            'amount':amount
        }
        url = "https://api.iamport.kr/payments/prepare"
        headers = {
            'Authorization':access_token
        }
        req = requests.post(url, data=access_data, headers=headers)
        # json 데이터로 파싱
        res = req.json()
        if res['code'] != 0:
            raise ValueError("API 통신 오류")
    else:
        raise ValueError("토큰 오류")


# 결제가 이뤄지면 iamport 에 기록이 남고 django app으로 결제 완료된 정보를 전송해준다.
# 주의할 점은 실제 결제 완료된 금액과 django app에서 결제된 금액이 맞는지 확인해야함.
# 그 과정을 진행하는 함수
def find_transaction(order_id, *args, **kwargs):
    access_token = get_token()
    if access_token:
        url = "https://api.iamport.kr/payments/find/"+order_id
        headers = {
            'Authorization':access_token
        }
        req = requests.post(url, headers=headers)
        res = req.json()
        if res['code'] == 0:
            context = {
                'imp_id':res['response']['imp_uid'],
                'merchant_order_id':res['response']['merchant_uid'],
                'amount':res['response']['amount'],
                'status':res['response']['status'],
                'type':res['response']['pay_method'],
                'receipt_url':res['response']['receipt_url']
            }
            return context
        else:
            return None

    else:
        raise ValueError("토큰 오류")