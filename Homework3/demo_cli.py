from sockets.python3.server import Server
from sockets.python3.client import Client
# Test server
class MyServer(Server):
    def act_on(self, data, addr):
        return data.decode()

diy_server = MyServer(listening_address=("10.31.70.109", 11113))
diy_server.listen()

# Test client
diy_client = Client()
response, addr = diy_client.poll_server("Hello world", server=("10.31.70.109", 11113))
print(response, addr)