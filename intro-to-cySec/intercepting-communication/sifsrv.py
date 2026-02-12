import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", "40000"))

flag, _ = sock.recvfrom(1024)


print(flag)

network = Network(hosts={}, subnet="10.0.0.0/24")

