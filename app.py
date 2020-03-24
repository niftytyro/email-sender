from flask import Flask
import email_sender

app = Flask(__name__)


##########Enter sender email here########
sender=""          
pw = ""            
##########Enter password here############


htmlFile = open("otp.html")
html=htmlFile.read()
body = {
    "subject": "Verification Code",
    "html": html
}


@app.route('/', methods=['GET'])
def home(name=None, receiver=None):
    if(name==None and receiver==None):
        return "Error 00392: No name and receiver specified"
    else:
        code = email_sender.sendOTP(sender, pw, receiver, name, body)
        return code



if(__name__=="__main__"):
    app.run()