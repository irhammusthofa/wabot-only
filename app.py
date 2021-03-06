import os, sys, time, json
import datetime
from webwhatsapi import WhatsAPIDriver, WhatsAPIDriverStatus
from webwhatsapi.objects.message import Message
from pathlib import Path
import requests
from requests.auth import HTTPBasicAuth
import json

def update(arr):
    try:
        url = 'http://localhost:5000/messages'
        myobj = {"_id":arr}
        print(myobj)
        x = requests.put(url,json=myobj)
    except Exception as e:
        print('Error:' + str(e))

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
    try:
        status_driver = driver.get_status()
        if (status_driver==WhatsAPIDriverStatus.LoggedIn):
            url = "http://localhost:5000/messages"
            myResponse = requests.get(url, verify=True).json()
            # For successful API call, response code will be 200 (OK)
            arr_id = []
            if(len(myResponse) > 0):
                jData = myResponse
                for key in jData:
                    id = key['_id']
                    to = key['Phone']
                    msg = key['Message']
                    arr_id.append(id)
                    print("Send Message '" + str(msg) +"' to " + str(to))
                    send_msg = driver.send_message_to_id(str(to)+"@c.us",str(msg))

                if len(arr_id) > 0:
                    update(arr_id)
                
                
    except Exception as e:
        print("Error:" + str(e))

def wabot_loop(driver):
    while True:
        time.sleep(10)
        wabot(driver)
            
init()
