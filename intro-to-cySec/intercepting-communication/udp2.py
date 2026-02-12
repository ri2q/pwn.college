import socket


ip = "10.0.0.2"
port = 31337

msg = "Hello, World!"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("10.0.0.1", 31338))


sock.sendto(msg, (ip, port))
