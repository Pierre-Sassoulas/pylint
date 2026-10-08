from pylxd import Client

client = Client()
print(client.instances)

print(client.virtual_machines)
print(dir(client.virtual_machines))
print(client.virtual_machines.all())
