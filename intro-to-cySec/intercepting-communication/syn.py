import socket, struct

def checksum(data: bytes) -> int:
    """Compute Internet Checksum (RFC 1071)"""
    s = 0
    # add 16-bit words
    for i in range(0, len(data), 2):
        w = (data[i] << 8) + (data[i+1] if i+1 < len(data) else 0)
        s += w
        s = (s & 0xffff) + (s >> 16)
    return ~s & 0xffff


# ======================
# IP Header Parameters
# ======================
src_ip = "10.0.0.1"
dst_ip = "10.0.0.2"

# ======================
# TCP Header Parameters
# ======================
src_port = 12345
dst_port = 31337
seq_num = 0
ack_num = 0
offset_res = (5 << 4) + 0
tcp_flags = 0x02   # SYN flag
window = 5840
urgent_ptr = 0

# ----------------------
# Build TCP Header (checksum=0 first)
# ----------------------
tcp_header = struct.pack("!HHLLBBHHH",
                         src_port, dst_port,
                         seq_num, ack_num,
                         offset_res, tcp_flags,
                         window, 0, urgent_ptr)

# Pseudoheader for checksum
src_ip_bytes = socket.inet_aton(src_ip)
dst_ip_bytes = socket.inet_aton(dst_ip)
placeholder = 0
protocol = socket.IPPROTO_TCP
tcp_length = len(tcp_header)

pseudo_header = struct.pack("!4s4sBBH",
                            src_ip_bytes, dst_ip_bytes,
                            placeholder, protocol, tcp_length)

tcp_checksum = checksum(pseudo_header + tcp_header)

# Rebuild TCP header with correct checksum
tcp_header = struct.pack("!HHLLBBH",
                         src_port, dst_port,
                         seq_num, ack_num,
                         offset_res, tcp_flags,
                         window) + struct.pack("H", tcp_checksum) + struct.pack("!H", urgent_ptr)


# ----------------------
# Build IP Header
# ----------------------
ip_ver = 4
ip_ihl = 5
ip_ver_ihl = (ip_ver << 4) + ip_ihl
ip_tos = 0
ip_tot_len = 20 + len(tcp_header)
ip_id = 54321
ip_frag_off = 0
ip_ttl = 64
ip_proto = socket.IPPROTO_TCP
ip_check = 0
ip_src = src_ip_bytes
ip_dst = dst_ip_bytes

ip_header = struct.pack("!BBHHHBBH4s4s",
                        ip_ver_ihl, ip_tos, ip_tot_len,
                        ip_id, ip_frag_off,
                        ip_ttl, ip_proto, ip_check,
                        ip_src, ip_dst)

# Calculate IP checksum
ip_check = checksum(ip_header)

# Rebuild IP header with checksum
ip_header = struct.pack("!BBHHHBBH4s4s",
                        ip_ver_ihl, ip_tos, ip_tot_len,
                        ip_id, ip_frag_off,
                        ip_ttl, ip_proto, ip_check,
                        ip_src, ip_dst)


# ======================
# Final Packet
# ======================
packet = ip_header + tcp_header

# ======================
# Send with raw socket
# ======================
sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
sock.sendto(packet, (dst_ip, 0))

print("SYN packet sent to", dst_ip)

