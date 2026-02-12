from scapy.all import IP, TCP, sr1, send, sr, conf, Raw


ip = IP(dst="10.0.0.2")
SYN = TCP(sport=31337, dport=31337, seq=31337, flags="S")
SYNACK = sr1(ip/SYN)

client = SYN.seq + 1
server = SYNACK.seq + 1

ACK = TCP(dport=31337, sport=31337, seq=client, ack=server, flags="A")

send(ip/ACK)



