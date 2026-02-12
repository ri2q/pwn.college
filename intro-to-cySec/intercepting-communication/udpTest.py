# udp_send_and_recv.py
import socket

dst_ip = "10.0.0.2"
dst_port = 31337
local_port = 31338

msg = b"Hello, World!\n"   # newline required by the server

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# bind to the required source port (you can bind to 0.0.0.0 or to 10.0.0.1)
sock.bind(("10.0.0.1", local_port))  

# send and then wait for the reply (server will send the flag back to our port)
sock.sendto(msg, (dst_ip, dst_port))

sock.settimeout(3.0)
try:
    data, addr = sock.recvfrom(4096)
    print("Received:", data.decode(errors="ignore"))
except socket.timeout:
    print("No response (timeout).")
finally:
    sock.close()

