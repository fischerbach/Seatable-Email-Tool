from seatable_api import Base, context

server_url = context.server_url or 'https://cloud.seatable.io' #replace with your instance URL
api_token = context.api_token or 'KEY'


base = Base(api_token, server_url)
base.auth()


contacts = base.filter('Contacts', 'Welcome = false')
for contact in contacts:
    print(contact)

update_row_data = {'Welcome': True}
updated_rows = contacts.update(update_row_data)
