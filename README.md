# Temperature-Alert-using-IOT-ML
Ever thought that you receive a Alert message on your phone when Temperature cross threshold value in Industrial plant.
Temperature Monitoring is the most important measurement parameters that is always used for monitoring and controlling in Industries.

#Things used in our project:

#Hardwares required
1)Bolt module 
2)Bread board
3)Buzzer
4)Male to female jumper wires
5)LM35 Sensor

#Softwares required
1)Twilio
2)Bolt cloud
3)Pycharm

#Hardware Setup:
step 1- Firstly We took Bread board for connections.
step 2- Just hold the LM35 sensor in a manner such that you can read LM35 written on it.
step 3- Then, you just need to identify the pins of the sensor as VCC,output and ground from your left to right.
step 4- Take male to female wire,connect the 3 pins of the LM35 to the bolt wifi module as follows:
        *VCC pin of the LM35 connects to 5V of the Bolt wifi module.
        *Ouput pin of the LM35 connects to A0(analog input pin) of the bolt wifi-module.
        *Ground pin of the LM35 connects o the ground.
        *Lastly, Take short pin of buzzer and connect it with ground and long pin with digital pin 0.
       
#Software programming
        Step-1 *Create a file named conf.py which will store all the credentials related to Twilio. To create a new file type sudo nano conf.py in the terminal. After that write below code to save all the credentials in a single file.

SID = 'AC5645f61df50abd639026df881e89daa1' 
AUTH_TOKEN = 'e2024f1d108687efe19db34a74443bee' 
FROM_NUMBER = '+17032918270'
TO_NUMBER = '+919749522710'
API_KEY = '2f794fd6-f7e3-413c-8dbf-eff43f335184'
DEVICE_ID = BOLT6907221' 

NOTE-We store all the credentials in a separate file since it is sensitive data which should not be shared with anyone. Hence it is a good practice to avoid using credentials in code directly. After replacing all the values, save the file using CTRL+X.

      Step-2 *Now create one more file named temp_sms.py. To do so you have to type sudo nano temp_sms.py in the terminal. Now we will write main code to collect the data from the Bolt and send SMS if it crosses the threshold.

The algorithm for the code can be broken down into the following steps - 

*Fetch the latest sensor value from the Bolt device.
*Check if the sensor value is in the range specified in our min and max values.
*If it is not in range, send the SMS.
*Wait for 10 seconds.
*Repeat from step 1.


CODE EXPLAINATION:
        *In the code, we first have to import our conf file which has all the credentials. The python json and time libraries are also imported in the same line. Since we have saved our conf file with the .py extension, we can directly import it.
                                   import conf, json, time
                                   
        *json is a python library used for handling all operations on JSON objects. JSON is nothing but a data communication format widely used on the Internet for sending/receiving data between a client and server. More information on JSON can be found here. Remember, 'json' is the python library used for handling JSON objects and JSON is a data communication format. 
        
        *Now we will import Bolt python library which will let us fetch the data stored in Bolt Cloud. To send the SMS, the Sms library is also imported. The below line of code imports the required libraries.
                                   from boltiot import Sms, Bolt
                                   
        *In the above line, we are importing two objects. First one is SMS which will be used to send SMS alerts and the other one is Bolt which is used for accessing data from your Bolt device like the temperature reading.
        
        *Now we will initialize two variables which will store minimum and maximum threshold value. You can initialize any minimum and maximum integer limits to them.
        
        *This would send an alert if the temperature reading goes below the minimum limit or goes above the maximum limit similar to the alerts on a Pharmaceutical company's manufacturing line.
               minimum_limit = 300 
               maximum_limit = 600
               
       *Now to fetch the data from Bolt Cloud, we will create an object called 'mybolt' using which you can access the data on your Bolt.
       
       *For the Bolt Cloud to identify your device, you will need to provide the API key and the Device ID when creating the mybolt object. Since the conf file holds the API key and Device ID variables, you can use them as follows,
              mybolt = Bolt(conf.API_KEY, conf.DEVICE_ID)
The above code will automatically fetch your API key and Device ID that you have initialized in conf.py file.
       *Now to send an SMS, we will create an object of the same.
              sms = Sms(conf.SID, conf.AUTH_TOKEN, conf.TO_NUMBER, conf.FROM_NUMBER)
The above code will automatically fetch your SID, AUTH_TOKEN, TO_NUMBER and FROM_NUMBER that you have initialized in conf.py file.

       *Since we want to continuously monitor the temperature reading, we will enclose our logic to fetch, compare and send the SMS inside an infinite loop using the `while True:` statement. An infinite loop is a special loop which executes its code continuously since its exit condition is never going to be valid. To exit the loop, we will need to forcibly exit the code by holding CTRL + C.
while True: 
    print ("Reading sensor value")
    response = mybolt.analogRead('A0') 
    data = json.loads(response) 
    print("Sensor value is: " + str(data['value']))
    try: 
        sensor_value = int(data['value']) 
        if sensor_value > maximum_limit or sensor_value < minimum_limit:
            print("Making request to Twilio to send a SMS")
            response = sms.send_sms("The Current temperature sensor value is " +str(sensor_value))
            print("Response received from Twilio is: " + str(response))
            print("Status of SMS at Twilio is :" + str(response.status))
    except Exception as e: 
        print ("Error occured: Below are the details")
        print (e)
    time.sleep(10)
    
      *The code continuously fetches the temperature value using `analogRead` function. Since the sensor is connected to A0 pin of the Bolt, we will execute the analogRead() function on the pin A0.The response from the Bolt Cloud using the analogRead() function is in a JSON format, so we will need to load the JSON data sent by the cloud using Python's json library.
      
      *The temperature value is inside a field labelled as "value" in the response. We can access the JSON values using the statement `sensor_value = int(data['value'])`. This line also converts the sensor reading to integer data type for comparing the temperature range.This is enclosed inside a try-except block to handle any error that may occur in the code. 
      
      *The next line of code checks if the temperature reading is above the maximum limit or below the minimum limit. If it exceeds, then the SMS will be sent.The SMS to be sent will contain the text "The Current temperature sensor value is" followed by the temperature value.The response from Twilio will be stored inside the `response` variable.
      
      *Once the temperature reading has been sent, we will need to wait for 10 seconds to get the next reading. For this, we will put the program to sleep once every loop iteration.The statement `time.sleep(10)` puts the program execution on hold for 10 seconds. This means that the program would not execute for a period of 10 seconds.
      
      *In the above code, we are fetching the data every 10sec. You can change the value but ideally, it should be good if the time interval between 2 data points is more than 10sec.
      
      *Note: The above "sensor_value" is the raw temperature reading, obtained from the LM35 sensor. In case you want to convert this value to the temperature in degree Celsius, use the formula: 
              Temperature=(100*sensor_value)/1024
              
      *Where sensor_value is the variable in which data obtained from the LM35 sensor is stored.Save the file. Time to run the code. To do so type `sudo python3 temp_sms.py` in terminal
      
      #FOR PREDICTION
      1)complete the connections as described in hardware setup,Power up the circuit and let it connect to the Bolt Cloud. (The Green LED of the Bolt should be on)
      2)Go to cloud.boltiot.com and create a new product. While creating the product, choose product type as Input Device and interface type as GPIO. After creating the product, select the recently created product and then click on configure icon.
      3)In the hardware tab, select the radio button next to the A0 pin. Give the pin the name 'temp' and save the configuration using the 'Save' icon.
      4) Move to the code tab, give the product code the name 'predict', and select the code type as js.
      5)Write the following code to plot the temperature data and run the polynomial regression algorithm on the data, and save the product configurations.

setChartLibrary('google-chart');
setChartTitle('Polynomial Regression');
setChartType('predictionGraph');
setAxisName('time_stamp','temp');
mul(0.0977);
plotChart('time_stamp','temp');
       6)In the products tab, select the product created and then click on the link icon. Select your Bolt device in the popup and then click the 'Done' button.
       7)Click on 'deploy configuration' button and then the 'view this device' icon to view the page that you have designed.
       8)Wait for about 2 hours for the device to upload enough data point to the Cloud. You can then click on the predict button to view the prediction graph based on polynomial regression algorithm.
