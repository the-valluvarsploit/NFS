import requests
import time
import datetime
import os
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0'}
slack_webhook = os.environ["SLACK_WEBHOOK"]
whatsapp_api_key = os.environ["WHATSAPP_API_KEY"]
channel_number = os.environ["CHANNEL_NUMBER"]
send_sms_to_numbers = os.environ["SEND_SMS_TO_NUMBERS"]  # 9197******20,9186*****44,9163******38


def get_manali_credits(username, password):
    URL = os.environ["MANALI_API_ENDPOINT"]
    params = {'user': username, 'password' : password}

    creditResponse = requests.get(URL, params=params, headers=headers)

    if creditResponse.status_code == 200:
        jsonCreditResponse = creditResponse.json()
        creditsAll = jsonCreditResponse['Balance']
        promoPart = creditsAll.split('|')[0]
        promoCredit = promoPart.split(':')[1]
        TransPart = creditsAll.split('|')[1]
        TransCredit = TransPart.split(':')[1]
        # print(f"{username} = {str(creditsPromo)} | {str(creditsTrans)}\n")
       
        if username == "netfishv":
            if int(TransCredit) < 200000:
                whatsapp_notify(username, TransCredit)
        elif username == "netyfish1":
            if int(TransCredit) < 200000:
                whatsapp_notify(username, TransCredit)
        elif username == "nettytrans":
            if int(TransCredit) < 200000:
                whatsapp_notify(username, TransCredit)
        elif username == "netyfish":
            if int(TransCredit) < 200000:
                whatsapp_notify(username, TransCredit)
        elif username == "netypromo":
            if int(promoCredit) < 200000:
                whatsapp_notify(username, promoCredit)
        elif username == "netpromo":
            if int(promoCredit) < 200000:
                whatsapp_notify(username, promoCredit)

    return username, creditsAll


def whatsapp_notify(username, balance):
    whatsapp_url = f"https://api.wacto.app/api/v1.0/messages/send-template/{channel_number}"
    payload = json.dumps({
              "messaging_product": "whatsapp",
              "recipient_type": "individual",
              "to": send_sms_to_numbers,
              "type": "template",
              "template": {
                 "name": "sms_low_credits_notification",
                 "language": {
                    "code": "en"
              },
            "components": [
              {
                "type": "body",
                "parameters": [
                    {
                        "type": "text",
                        "text": username
                    },
                    {
                        "type": "text",
                        "text": balance
                    }
                ]
             }
           ]
          }
         })
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {whatsapp_api_key}'
    }

    response = requests.post(whatsapp_url, headers=headers, data=payload)
    # print(response.text)
    
    
def main():
    tempDate = datetime.datetime.now()
    currentDate = tempDate.strftime("%d-%m-%Y %H:%M:%S")
    print(f"\n-----------------{currentDate}---------------------\n")
    print("Credits Update:\n")

    ntfv_username = os.environ["NTFV_USERNAME"]  # netfishv
    ntfv_password = os.environ["NTFV_PASSWORD"]
    ntf1_username = os.environ["NTF1_USERNAME"]  # netyfish1
    ntf1_password = os.environ["NTF1_PASSWORD"]
    ntftrans_username = os.environ["NTFTRANS_USERNAME"]  # nettytrans
    ntftrans_password = os.environ["NTFTRANS_PASSWORD"]
    ntfpromo_username = os.environ["NTFPROMO_USERNAME"]  # netypromo
    ntfpromo_password = os.environ["NTFPROMO_PASSWORD"]
    ntfpromo2_username = os.environ["NTFPROMO2_USERNAME"] # netpromo
    ntfpromo2_password = os.environ["NTFPROMO2_PASSWORD"]
    netyfish_username = os.environ["NETYFISH_USERNAME"]  # netyfisht
    netyfish_password = os.environ["NETYFISH_PASSWORD"]

    username1, credits_ntfv = get_manali_credits(ntfv_username, ntfv_password) # netfishv
    time.sleep(5)
    username2, credits_ntf1 = get_manali_credits(ntf1_username, ntf1_password)  # netyfish1
    time.sleep(5)
    username3, credits_ntftrans = get_manali_credits(ntftrans_username, ntftrans_password)   # nettytrans
    time.sleep(5)
    username4, credits_ntfpromo = get_manali_credits(ntfpromo_username, ntfpromo_password)  # netypromo
    time.sleep(5)
    username10, credits_ntfpromo2 = get_manali_credits(ntfpromo2_username, ntfpromo2_password)  # netpromo
    time.sleep(5)
    username11, credits_netyfish = get_manali_credits(netyfish_username, netyfish_password)  # netyfisht

    print(f"\n---------------------------------------------------\n")

    payload = {
    'text': '<!channel>, Credits Update:\n\n' +
            '*Manali:*' + '\n' +
            username1 + ' (SS) = ' + str(credits_ntfv) + '\n\n' + # netfishv
            username2 + ' (RS) = ' + str(credits_ntf1) + '\n\n' + # netyfish1
            username3 + ' (RS) = ' + str(credits_ntftrans) + '\n\n' + # nettytrans
            username4 + ' (RS) = ' + str(credits_ntfpromo) + '\n\n' + # netypromo
            username10 + ' (SS) = ' + str(credits_ntfpromo2) + '\n\n' + # netpromo
            username11 + ' (SS) = ' + str(credits_netyfish) + '\n\n' # netyfisht
    }

    requests.post(slack_webhook, json= payload, headers={'content-type': 'application/json'})

main()
