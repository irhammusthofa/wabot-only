import os, sys, time, json
import datetime
from webwhatsapi import WhatsAPIDriver, WhatsAPIDriverStatus
from webwhatsapi.objects.message import Message
import mysql.connector
from mysql.connector import Error
from pathlib import Path

def init():
    try:
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
    except Error as e:
        print("Error : ",e)
        print("restarting...")
        driver.close()
        init()

def wabot(mydb,driver):
    try:
        sql = "SELECT * FROM outbox_whatsapp WHERE ow_status=0 ORDER BY ow_created ASC LIMIT 100"
        if (mydb.is_connected()):
            now = datetime.datetime.now()
            now = now.strftime("%Y-%m-%d %H:%M:%S")
            print("check outbox" + str(now))
            status_driver = driver.get_status()
            is_connected = False
            if (status_driver==WhatsAPIDriverStatus.LoggedIn):
                mycursor = mydb.cursor()
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                for row in myresult:
                    id = row[0]
                    to = row[2]
                    msg = row[3]
                    print("Send Message '" + str(msg) +"' to " + str(to))

                    #send whatsapp
                    #if (is_connected==True):
                    send_msg = driver.send_message_to_id(str(to)+"@c.us",str(msg))
                    print("status msg : ", send_msg)
                        #update db
                    sql_update = "UPDATE outbox_whatsapp SET ow_status=1, ow_send_time='" + str(now) + "' WHERE ow_id=" + str(id)
                    mycursor.execute(sql_update)
                    mydb.commit()
                    #else:
                    #    print("WhatsApp tidak terhubung")

            mycursor.close()
            mydb.close()
    except Error as e:
        print("Error : ",e)
        print("restarting...")
        driver.close()
        init()
def wabot_loop(driver):
    while True:
        time.sleep(10)
        try:
            mydb = mysql.connector.connect(
                host="host",
                user="user_db",
                passwd="pass_db",
                database="db"
            )
        except Error as e:
            print("Error Connection",e)
            print("restarting...")
            driver.close()
            init()
            break
        finally:
            wabot(mydb,driver)
init()
