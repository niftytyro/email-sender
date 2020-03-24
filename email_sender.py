import ssl, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os, random


def sendOTP(sender, pw, receiver_address, name, body):
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_address = sender
    
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

    context = ssl.create_default_context()

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_address, pw)
        server.sendmail(sender_address, receiver_address, message.as_string())
        return code
    except Exception as e:
        print(e)
    finally:
        server.quit()
