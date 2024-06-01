from tcp_client import Client

clients = []
for i in range(100):
    client = Client("127.0.0.1", 42424, 0.6)
    client.start_client(i)
    clients.append(client)

print(clients)