# -*- coding: utf-8 -*-
import smtplib, os, socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email import encoders

def sendMail(sender, receiver, password, host, port, file):
    """wysyła wiadomość email z załącznikiem"""
    file = os.path.join(file)
    head, tail = os.path.split(file)
    mail_content = '''W załączniku plik metadanych:
    %s''' % tail


    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = "Wtyczka APP QGIS"
    message['To'] = receiver
    message['Subject'] = 'Plik metadanych z wtyczki APP QGIS - %s' % tail
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))

    try:
        attach_file = MIMEApplication(open(file, "rb").read())
    except FileNotFoundError:
        return False, "Błąd odczytu pliku. Nie można wysłać pliku: %s" % file
    attach_file.add_header('Content-Disposition', 'attachment', filename=tail)
    message.attach(attach_file)

    #Create SMTP session for sending the mail
    try:
        with smtplib.SMTP(host, port, timeout=10) as session:
            session.starttls() #enable security
            session.login(sender, password) #login with mail_id and password
            text = message.as_string()
            session.sendmail(sender, receiver, text)
    except smtplib.SMTPServerDisconnected:
        return False, "Przekroczono czas połączenia z serwerem"
    except smtplib.SMTPAuthenticationError:
        return False, "Niepoprawny użytkownik lub hasło do serwera SMTP"
    except smtplib.SMTPRecipientsRefused:
        return False, "Niepoprawny adres odbiorcy"
    except socket.gaierror:
        return False, "Nie można nawiązać połączenia z hostem: %s poprzez port %s" % (host, port)
    except socket.timeout:
        return False, "Przekroczono czas połączenia z serwerem, sprawdź port"
    return [True]


if __name__ == "__main__":
    res = sendMail(sender="",
             receiver="",
             password="",
             host="mail.envirosolutions.pl",
             port="587",
             file="")
    print(res)