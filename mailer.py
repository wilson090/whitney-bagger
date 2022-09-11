import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "wilsondevmailer@gmail.com"  # Enter your address
receiver_email = "wilsonspearman@gmail.com"  # Enter receiver address


def retrieve_password():
    password = os.environ.get('password', None)

    if password:
        return password

    with open('super_secure_password.txt') as f:
        return f.read().strip("\n")


def send_email_notification(dates):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Whitney Alert"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = f"""\
    Whitney permit(s) available overnight: {", ".join(dates["overnight"])} and day use: {", ".join(dates["day_use"])}. Link: https://www.recreation.gov/permits/233260"""
    html = f"""\
    <html>
      <body>
        <h2>Whitney permit(s) available!</h2>
        <p>
           <b>Overnight:</b> {", ".join(dates["overnight"])}<br>
           <b>Day use:</b> {", ".join(dates["day_use"])}<br><br>
           <a href="https://www.recreation.gov/permits/233260">Link to reserve</a> 
        </p>
      </body>
    </html>
    """
    message.attach(MIMEText(text, "plain"))
    message.attach(MIMEText(html, "html"))

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, retrieve_password())
        server.sendmail(sender_email, receiver_email, message.as_string())
