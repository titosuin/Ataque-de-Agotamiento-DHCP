# Ataque-de-Agotamiento-DHCP
#  DHCP Starvation Tool (DoS)

![Type](https://img.shields.io/badge/Attack-DoS-red)
![Protocol](https://img.shields.io/badge/Protocol-DHCP-blue)
![Status](https://img.shields.io/badge/Status-Educational-orange)

Herramienta de auditoría de red diseñada para probar la resiliencia de servidores DHCP ante ataques de agotamiento de recursos (Starvation). El script genera miles de solicitudes DHCP DISCOVER falsificadas con direcciones MAC aleatorias para consumir la totalidad del pool de direcciones IP disponibles.

##  Objetivo del Script
Demostrar la vulnerabilidad de un servidor DHCP que no cuenta con mecanismos de validación de identidad (como Port Security). El objetivo es denegar el servicio a nuevos clientes legítimos impidiendo que obtengan una dirección IP.

## Topología y Escenario

El ataque se ejecuta en un entorno controlado GNS3 sobre la **VLAN 2295**.

* **Segmento de Red:** `10.22.95.0/24`
* **VLAN ID:** 2295
* **Gateway (Víctima DoS):** Router Cisco (`10.22.95.1`)
* **Atacante:** Kali Linux (`eth0`)

| Dispositivo | Rol | Estado Inicial |
| :--- | :--- | :--- |
| **Router Gateway** | Servidor DHCP | Pool activo (~250 IPs libres) |
| **Switch L2** | Infraestructura | Puertos de acceso sin seguridad |
| **Kali Linux** | Atacante | Generador de tráfico |

><img width="678" height="716" alt="image" src="https://github.com/user-attachments/assets/4ccd36c8-c0a3-484e-a67d-ca9d7416ba36" />

> *Figura 1: Diagrama de red mostrando la conexión del atacante al puerto de acceso.*

##  Parámetros Técnicos Usados

El script utiliza la librería **Scapy** para la inyección de paquetes en capa 2/3.

* **Interfaz de Inyección:** `eth0`
* **Generación de MAC:** Función `RandMAC()` para aleatoriedad criptográfica.
* **Estructura del Paquete:**
    * `Ethernet`: Src=Random / Dst=Broadcast (`ff:ff:ff:ff:ff:ff`)
    * `IP`: Src=`0.0.0.0` / Dst=`255.255.255.255`
    * `UDP`: Sport=68 / Dport=67
    * `BOOTP`: Client Hardware Address (chaddr) aleatorio.
    * `DHCP Options`: Message-Type = `Discover`.

##  Evidencia de Ejecución

**1. Ejecución del Script:**
><img width="566" height="124" alt="image" src="https://github.com/user-attachments/assets/4a672c65-58f3-4946-87e9-df70540a97e6" />

> *El script envía solicitudes masivas en bucle.*

**2. Impacto en el Servidor (DoS Logrado):**

<img width="640" height="503" alt="image" src="https://github.com/user-attachments/assets/a08d09e6-4d7b-4330-ade5-6fa74dfd417f" />

> *La tabla de asignaciones DHCP está saturada con direcciones MAC falsas.*

##  Requisitos

* Python 3.x
* Librería Scapy (`pip install scapy`)
* Permisos de Superusuario (Root/Sudo)

##  Medidas de Mitigación

Para prevenir este ataque, se debe configurar **Port Security** en los switches de acceso para limitar el número de direcciones MAC permitidas por puerto.

```bash
Switch(config)# interface range e0/0-3
Switch(config-if)# switchport port-security
Switch(config-if)# switchport port-security maximum 2
Switch(config-if)# switchport port-security violation restrict
