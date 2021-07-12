from seatable_api import Base
from seatable_api.constants import UPDATE_DTABLE
import json

server_url = 'https://cloud.seatable.io'
api_token = 'KEY'

base = Base(api_token, server_url)
base.auth(with_socket_io=True)

def on_update_seatable(data, index, *args):
    try:
        data = json.loads(data)
    except:
        print("Something went wrong with data decode.")
        return

    print(data)

base.socketIO.on(UPDATE_DTABLE, on_update_seatable)
base.socketIO.wait()  # forever
