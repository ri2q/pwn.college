import socket, time


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("10.0.0.3", 31337))


msg =  bytes("FLAG:10.0.0.1:40000\n", "UTF-8")


for i in range(1, 65535):
    try:
        sock.sendto(msg, ("10.0.0.2", i))
        time.sleep(0.001)
    except Exception as e:
        print("err: ", i, e)


sock.close()


