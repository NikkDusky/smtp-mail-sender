import os
import time
import smtplib
from configparser import ConfigParser
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

parser = ConfigParser()
parser.read('settings.ini')

Login = parser.get('auth', 'login')
Password = parser.get('auth', 'password')

smtp_domain = parser.get('smtp_settings', 'domain')
smtp_port = parser.get('smtp_settings', 'port')


if parser.get('mail', 'time_instead_of_topic') == "True":
    Theme = time.strftime("%d %B %Y / %H-%M-%S", time.localtime())
else:
    Theme = parser.get('mail', 'theme')

Send_To = parser.get('mail', 'send_to')

def SendMail(Text):
    msg = MIMEMultipart()
    msg['Subject'] = Theme
    msg['From'] = Login
    msg['To'] = Send_To

    text = MIMEText(Text)
    msg.attach(text)

    s = smtplib.SMTP(f'{smtp_domain}: {smtp_port}')
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(Login, Password)
    s.sendmail(Login, Send_To, msg.as_string().encode("UTF-8"))
    s.quit()

def SendMailWithImage(ImgFileName, Text):
    with open(ImgFileName, 'rb') as f:
        img_data = f.read()

    msg = MIMEMultipart()
    msg['Subject'] = Theme
    msg['From'] = Login
    msg['To'] = Send_To

    text = MIMEText(Text)
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
    msg.attach(image)

    s = smtplib.SMTP(f'{smtp_domain}: {smtp_port}')
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(Login, Password)
    s.sendmail(Login, Send_To, msg.as_string().encode("UTF-8"))
    s.quit()