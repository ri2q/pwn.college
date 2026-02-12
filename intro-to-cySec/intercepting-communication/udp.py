import socket

uIp = "10.0.0.2"
uPort = 31337
msg = "Hello, World!"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.sendto(bytes(msg, "utf-8"), (uIp, uPort))

