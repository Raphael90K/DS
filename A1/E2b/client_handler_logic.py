from tcp_client import Client

clients = []
for i in range(10):
    client = Client("79.214.184.93", 42424, 0)
    client.start_client(i)
    clients.append(client)

print(clients)