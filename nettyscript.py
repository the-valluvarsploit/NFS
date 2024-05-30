import requests
import time
import datetime
import os

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0'}
slack_webhook = os.environ["SLACK_WEBHOOK"]

def get_bsnl_credits(URL, userid, password):
    URL = URL + "/SMSApi/account/readstatus"
    params = {'userid': userid, 'password': password, 'output': 'json'}

    creditResponse = requests.get(URL, params=params, headers=headers)

    if creditResponse.status_code == 200:
        jsonCreditResponse = creditResponse.json()
        credits = jsonCreditResponse['response']['account']['smsBalance']
        # print(userid + " = " + str(credits))
        print(f"{userid} = {credits}\n")

    return userid, credits




def get_manali_credits(username, password):
    URL = os.environ["MANALI_API_ENDPOINT"]
    params = {'user': username, 'password' : password}

    creditResponse = requests.get(URL, params=params, headers=headers)

    if creditResponse.status_code == 200:
        jsonCreditResponse = creditResponse.json()
        creditsAll = jsonCreditResponse['Balance']
        creditsPromo = creditsAll.split('|')[0]
        creditsTrans = creditsAll.split('|')[1]
        # print(username + " = " + str(creditsAll))
        print(f"{username} = {str(creditsPromo)} | {str(creditsTrans)}\n")

    return username, creditsAll


def get_dategen_credits(username, password):
    url = os.environ["DATAGEN_URL"]
    loginEndpoint = "/apismpp/v1/login.php"
    loginParams = {'username': username, 'password': password}

    loginResponse = requests.get(url + loginEndpoint, params=loginParams, headers=headers)

    if loginResponse.status_code == 200:
        jsonLoginResponse = loginResponse.json()
        name = jsonLoginResponse['user']['name']
        token = jsonLoginResponse['user']['token']
        type = jsonLoginResponse['user']['type']
 
    creditEndpoint = "/apismpp/v1/users.php"
    creditParams = {'user_id': name, 'method': 'retrieve_profile', 'id': name, 'token': token, 'user_type': type}

    creditResponse = requests.get(url + creditEndpoint, params=creditParams, headers=headers)
        
    if creditResponse.status_code == 200:
        jsonCreditResponse = creditResponse.json()
        credits = jsonCreditResponse['data'][0]['credit']
        userName2 = jsonCreditResponse['data'][0]['username']
        # print(userName2 + " = " + str(credits))
        print(f"{userName2} = {str(credits)}\n")
    
    return userName2, credits
    
    
def main():
    tempDate = datetime.datetime.now()
    currentDate = tempDate.strftime("%d-%m-%Y %H:%M:%S")
    print(f"\n-----------------{currentDate}---------------------\n")
    print("Credits Update:\n")

    ntfv_username = os.environ["NTFV_USERNAME"]
    ntfv_password = os.environ["NTFV_PASSWORD"]
    ntf1_username = os.environ["NTF1_USERNAME"]
    ntf1_password = os.environ["NTF1_PASSWORD"]
    ntftrans_username = os.environ["NTFTRANS_USERNAME"]
    ntftrans_password = os.environ["NTFTRANS_PASSWORD"]
    ntfpromo_username = os.environ["NTFPROMO_USERNAME"]
    ntfpromo_password = os.environ["NTFPROMO_PASSWORD"]
    datagntf_username = os.environ["DATAG_NTF_USERNAME"]
    datagntf_password = os.environ["DATAG_NTF_PASSWORD"]
    datagntf2_username = os.environ["DATAG_NTF2_USERNAME"]
    datagntf2_password = os.environ["DATAG_NTF2_PASSWORD"]
    bsnl_ntftr8_url = os.environ["BSNL_NTFTR8_URL"]
    bsnl_ntftr8_username = os.environ["BSNL_NTFTR8_USERNAME"]
    bsnl_ntftr8_password = os.environ["BSNL_NTFTR8_PASSWORD"]
    bsnl_ntftr_url = os.environ["BSNL_NTFTR_URL"]
    bsnl_ntftr_username = os.environ["BSNL_NTFTR_USERNAME"]
    bsnl_ntftr_password = os.environ["BSNL_NTFTR_PASSWORD"]

    username1, credits_ntfv = get_manali_credits(ntfv_username, ntfv_password)
    time.sleep(5)
    # username2, credits_ntf1 = get_manali_credits(ntf1_username, ntf1_password)
    # time.sleep(5)
    # username3, credits_ntftrans = get_manali_credits(ntftrans_username, ntftrans_password)
    # time.sleep(5)
    # username4, credits_ntfpromo = get_manali_credits(ntfpromo_username, ntfpromo_password)
    # time.sleep(5)
    # username5, credits_datag_ntf = get_dategen_credits(datagntf_username, datagntf_password)
    # time.sleep(5)
    # username6, credits_datag_ntf2 = get_dategen_credits(datagntf2_username, datagntf2_password)
    # time.sleep(5)
    # username7, credits_ntftr8 = get_bsnl_credits(bsnl_ntftr8_url, bsnl_ntftr8_username, bsnl_ntftr8_password)
    # time.sleep(5)
    # username8, credits_ntftr = get_bsnl_credits(bsnl_ntftr_url, bsnl_ntftr_username, bsnl_ntftr_password)

    print(f"\n---------------------------------------------------\n")

    # payload = {
    # 'text': '<!channel>, Credits Update:\n\n' +
    #         username1 + ' = ' + str(credits_ntfv) + '\n\n' +
    #         username2 + ' = ' + str(credits_ntf1) + '\n\n' +
    #         username3 + ' = ' + str(credits_ntftrans) + '\n\n' +
    #         username4 + ' = ' + str(credits_ntfpromo) + '\n\n' +
    #         username5 + ' = ' + str(credits_datag_ntf) + '\n\n' +
    #         username6 + ' = ' + str(credits_datag_ntf2) + '\n\n' +
    #         username7 + ' = ' + str(credits_ntftr8) + '\n\n' +
    #         username8 + ' = ' + str(credits_ntftr) + '\n\n'
    # }

    payload = {
    'text': '<!channel>, Credits Update:\n\n' +
            username1 + ' = ' + str(credits_ntfv) + '\n\n'
    }


    requests.post(slack_webhook, json= payload, headers={'content-type': 'application/json'})
    
    
def run_every_hour():
    while True:
        main()
        # Sleep for half an hour (3600 seconds)
        time.sleep(3600)


if __name__ == "__main__":
    run_every_hour()