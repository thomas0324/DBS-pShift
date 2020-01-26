# DBS-pShift

![Screenshot (54)](https://user-images.githubusercontent.com/49776836/64486842-09d51480-d265-11e9-9b00-72c69f142ab5.png)


1. Setting up the environment 

    In order to run the prototype in your computer, you may need to install the libraries and framework in the requirments.txt file by
    typing this code

        pip install -r requirements.txt 
    
2. Facial Recgonition

    a. The database is the folder "faces" , which stores the customer's faceID

    b. The test case is the test image, if you want to test another person, just put your image to the folder and rename it as "test"

    You can run this program by typing the following command, 

        python face_rec.py

3. ChatBot

    a. The training set is the intents.json file , you can edit it and output the corresponding response

    You can run this program by typing the following command,
  
        python main.py

4. Email 

    a. The attachment is the "DBS ATM Receipt.png" 

    b. In the email-demo.py you can edit the code , so the attachment will be sent it to your email account.
  
        msg['To'] = 'youremail@gmail.com'

    You can run this program by typing the following command,

        python email-demo.py 
    
 
