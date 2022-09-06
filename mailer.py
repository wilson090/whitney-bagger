import smtplib
import ssl

port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "wilsondevmailer@gmail.com"  # Enter your address
receiver_email = "wilsonspearman@gmail.com"  # Enter receiver address


def retrieve_password():
    with open('super_secure_password.txt') as f:
        return f.read().strip("\n")


def send_email_notification(date, overnight=False):
    message = f"""\
    Subject: Whitney Alert
    
    Whitney {"overnight" if overnight else "day use"} permit available for {date}. Link: https://www.recreation.gov/permits/233260"""

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, retrieve_password())
        server.sendmail(sender_email, receiver_email, message)
