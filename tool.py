from seatable_api import Base, context
from seatable_api.constants import UPDATE_DTABLE
import json
from markdown import markdown

import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

server_url = context.server_url or 'https://cloud.seatable.io' #replace with your instance URL
api_token = context.api_token or 'KEY'

SMTPSERVER = 'smtp.mail.yahoo.com'
USERNAME = 'rafalrybnik@yahoo.com'
PASSWORD = 'INYOURDREAMS'
SENDER = 'rafalrybnik@yahoo.com'

base = Base(api_token, server_url)
base.auth()

def get_template(name):
    template = base.filter('Templates', f'Name = {name}')
    if len(template) < 1:
        raise Exception('Template not foud!')
    message = markdown(template[0]['Message'])
    return message

base_with_socket = Base(api_token, server_url)
base_with_socket.auth(with_socket_io=True)


def send_message(email, subject, message):
    msg = MIMEMultipart('mixed')
    msg['Subject'] = subject
    msg['From'] = f'{SENDER} <{SENDER}>'

    msg['To'] = email

    text_html = MIMEText(message,'html', 'utf-8')
    msg.attach(text_html)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTPSERVER, 465, context=context) as server:
        server.login(USERNAME, PASSWORD)
        server.sendmail(
            SENDER, email, msg.as_string()
        )
    

def on_update_seatable(data, index, *args):
    try:
        data = json.loads(data)
    except:
        print("Something went wrong with data decode.")
        return
    
    if (data['op_type'] == 'insert_row'):
        #find row
        row = base.get_row('Contacts', data['row_id'])
        message = get_template('Welcome')
        subject = 'Welcome!'

        #send email
        send_message(row['Email'], subject, message)

        #update column value
        base.update_row('Contacts', data['row_id'], {'Welcome': True})

base_with_socket.socketIO.on(UPDATE_DTABLE, on_update_seatable)
base_with_socket.socketIO.wait()  # forever
