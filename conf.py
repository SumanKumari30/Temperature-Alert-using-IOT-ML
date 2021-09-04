Python 3.7.4 (tags/v3.7.4:e09359112e, Jul  8 2019, 20:34:20) [MSC v.1916 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> import conf
from boltiot import Sms, Bolt
import json, time

maximum_limit = 600
minimum_limit = 300


mybolt = Bolt(conf.API_KEY, conf.DEVICE_ID)
sms = Sms(conf.SID, conf.AUTH_TOKEN, conf.TO_NUMBER, conf.FROM_NUMBER)


while True:
    print ("Reading sensor value")
    response = mybolt.analogRead('A0')
    data = json.loads(response)
    print("Sensor value is: " + str(data['value']))
    try:
        sensor_value = int(data['value'])
        if sensor_value > maximum_limit:
            response = mybolt.digitalWrite('0', 'HIGH')
            print("Making request to Twilio to send a SMS")
            response = sms.send_sms("DANGER!"+ str(sensor_value))
            print("Response received from Twilio is: " + str(response))
            print("Status of SMS at Twilio is :" + str(response.status))

        elif sensor_value < maximum_limit:
            response = mybolt.digitalWrite('0', 'LOW')
    except Exception as e:
        print ("Error occured: Below are the details")
        print (e)
    time.sleep(10)
