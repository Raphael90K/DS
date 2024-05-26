from tcp_client import Client

clients = []
for i in range(10):
    client = Client("127.0.0.1", 42424)
    client.start_client()
    clients.append(client)

print(clients)