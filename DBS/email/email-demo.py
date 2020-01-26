
import os
import smtplib 
from email.message import EmailMessage
import imghdr
import datetime
import boto3

EMAIL_ADDRESS = 'dbsemailtesting@gmail.com'
EMAIL_PASSWORD = 'March199703'
time = datetime.datetime.now()
time = str(time)

msg = EmailMessage()
msg['Subject'] = 'Withdrawal from ATM'
msg['From'] = EMAIL_ADDRESS
msg['To'] = 'yinli19970324@gmail.com'
msg.set_content('Dear Mr.Li Chun Yin,\n \nKindly be informed, your order to withdraw 10000 HKD is completed at ' + time + '\n\nPlease find the attachment below for your record.\n\nThanks for using our ATM services.\n\nDBS ATM services team')


with open('DBS ATM Receipt.png', 'rb') as f:
	file_data = f.read()
	file_type = imghdr.what(f.name)
	file_name = f.name

msg.add_attachment(file_data, maintype ='image', subtype = file_type, filename = file_name)



with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

	smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

	smtp.send_message(msg)


