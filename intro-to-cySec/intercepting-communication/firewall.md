iptables -I  INPUT -p tcp --dport `port` -j DROP >> 1
iptables -I  INPUT -s `adddres` -p tcp --dport `port` -j DROP >> 1
iptables -I  INPUT -p tcp --dport `port` -j DROP >> 1





