import smtplib
import ssl
import get_comments
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import configparser
import os

# Gets links using thread ids
def get_links():
    links = ""
    for id in get_comments.submission_ids:
        links += "<a href='http://www.reddit.com/" + id + "'>" + id + "</a><br>"
    return links

# Gets comments from get_comments
def get_text():
    with open(get_comments.file_name, "r") as comments:
        text = comments.read()
    return text

# Formats text and links as html 
def get_html(text):
    return """\
    <html>
    <head></head>
    <body>
        <p>
        """ + text.replace("\n", "<br>") + get_links() + """
        </p>
    </body>
    </html>
    """

# Sends comments from get_comments
def send_email():
    text = get_text()
    html = get_html(text)

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2) # runs this first - if it can't use html, uses plain text

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())

try:
    smtp_server = "smtp.gmail.com"
    port = 465
    sender = os.environ['sender'] 
    password = os.environ["sender_password"] 
    receiver = os.environ["receiver"]
    subject = "Your Daily Digest" 
except:
    print("Invalid config file")
else:
    send_email()

