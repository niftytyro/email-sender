import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os, random, re


def validate_email(email):
        if(len(email)):
            symbol = email.find('@')
            if(symbol<1):
                return False
            recipient = [0, symbol-1]
            if((len(email[recipient[0]:recipient[1]+1])<=64) and (len(email[recipient[0]:recipient[1]+1])>0)):
                tmp = re.findall("^[a-zA-z0-9]*[a-zA-z0-9!#\$%&'\*\+-/=?\^_`\{\}\|\"\(\),:;<>\[\]\.\\]*[a-zA-z0-9]*$", email[recipient[0]:recipient[1]+1])
            else:
                return False
            if(len(tmp)==0):
                return False
            domain = symbol+1           
            if((len(email[domain:])>3) and (len(email[domain:])<=253)):
                tmp = re.findall("^[a-zA-z0-9]*[a-zA-z0-9!#\$%&'\*\+-/=?\^_`\{\}\|\"\(\),:;<>\[\]\.\\]*[a-zA-z0-9]*$", email[domain:])
            return True
        return False

def sendOTP(sender, pw, receiver_address, name, body):
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_address = sender
    if(not validate_email(receiver_address)):
        return "EMAIL101"
    message = MIMEMultipart("alternative")
    message["Subject"] = body['subject']
    message["From"] = sender_address
    message["To"] = receiver_address

    text = """\
    Hi there!
    Final stages"""

    code = random.randint(1000, 10000)

    html=body['html']
    index = html.find(">otp")
    html = html[:index+1] + str(code) + html[index+4:]

    index = html.find(">name")
    html = html[:index+1] + name + html[index+4:]
    
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    # context = ssl.create_default_context()

    try:
        server = smtplib.SMTP(smtp_server, port)
        # server.ehlo()
        server.starttls()
        # server.ehlo()
        server.login(sender_address, pw)
        server.sendmail(sender_address, receiver_address, message.as_string())
        return str(code)
    except Exception as e:
        return e.message
    finally:
        server.quit()
