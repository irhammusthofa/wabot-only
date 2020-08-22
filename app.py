import os, sys, time, json
import datetime
from webwhatsapi import WhatsAPIDriver, WhatsAPIDriverStatus
from webwhatsapi.objects.message import Message
from pathlib import Path
import requests
from requests.auth import HTTPBasicAuth
import json

def update(arr):
    url = 'https://wa.golekonline.com/api1/message/outbox'
    myobj = {'id': json.dumps(arr)}
    x = requests.patch(url, data = myobj,auth=HTTPBasicAuth('what-bot','f0ba1f94ba5614a6c63357a5770a8e2707aab72e86e0ead124f769c7a7b5a1b0'))

def init():
    pathdir = Path(__file__).parent.absolute()
    profiledir= str(pathdir) + str("/firefox_cache")
    if not os.path.exists(profiledir): os.makedirs(profiledir)
    driver = WhatsAPIDriver( profile=profiledir,loadstyles=True)
    driver.driver.get(driver._URL)
    print("Waiting for QR")
    driver.wait_for_login()
    print("Saving session")
    driver.save_firefox_profile(remove_old=False)
    print("WhatsApp Ready")
    wabot_loop(driver)

def wabot(driver):
    if (status_driver==WhatsAPIDriverStatus.LoggedIn):
        url = "https://wa.golekonline.com/api1/message/outbox"
        myResponse = requests.get(url,auth=HTTPBasicAuth('what-bot','f0ba1f94ba5614a6c63357a5770a8e2707aab72e86e0ead124f769c7a7b5a1b0'), verify=True)
        # For successful API call, response code will be 200 (OK)
        arr_id = []
        if(myResponse.ok):
            jData = json.loads(myResponse.content)
            for key in jData:
                id = key['ow_id']
                to = key['ow_to']
                msg = key['ow_message']
                arr_id.append(id)
                print("Send Message '" + str(msg) +"' to " + str(to))
                send_msg = driver.send_message_to_id(str(to)+"@c.us",str(msg))
            
            update(arr_id)
        else:
            myResponse.raise_for_status()
            
def wabot_loop(driver):
    while True:
        time.sleep(10)
        wabot(driver)
            
init()
