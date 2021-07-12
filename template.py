from seatable_api import Base, context

server_url = context.server_url or 'https://cloud.seatable.io' #replace with your instance URL
api_token = context.api_token or 'KEY'


base = Base(api_token, server_url)
base.auth()

###1###
template = base.filter('Templates', 'Name = Welcome')
if len(template) < 1:
    raise Exception('Template not foud!')
template = template[0]
print(template['Message'])

###2###
from markdown import markdown
message = markdown(template['Message'])
print(message)
