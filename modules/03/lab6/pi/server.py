import socket
import asyncio
import websockets
import json

localPort = 8888
bufferSize = 1024

# AF_INET - Address family IPv4, meaning that socket will use 4-part IP address
# SOCK_DGRAM = Socket type is Datagram (UDP instead of TCP)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Websockets setup
clients = set()

# Light value state
NIGHT_CUTOFF = 0.75
DAY_CUTOFF = 0.25
current_state = "day"

DEBOUNCE_CUTOFF = 10
debounce_count = 30

# Websockets functions

async def handler(websocket):
    print("Client connected")
    
    clients.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)

            if data.get("request") == "get_state":
                await send_new_state()
    finally:
        clients.remove(websocket)
        print("Client disconnected")

async def send_new_state():
    packet = {
        "new_state": current_state
    }

    message = json.dumps(packet)

    print(f"Sending new state: {current_state}")

    for client in clients.copy():
        await client.send(message)

async def forward_light_values():
    global current_state, debounce_count

    while True:
        str_data, addr = await asyncio.to_thread(receive_from_socket)

        if not str_data:
            print("Received empty data")
            continue

        data = float(str_data)
        
        if current_state == "day":
            # Check if dark enough to turn to night
            if data > NIGHT_CUTOFF:
                debounce_count += 1
                if debounce_count >= DEBOUNCE_CUTOFF:
                    # Switch to night
                    current_state = "night"
                    debounce_count = 0
                    await send_new_state()
            else:
                debounce_count = 0
        else:
            # Check if light enough to turn to day
            if data < DAY_CUTOFF:
                debounce_count += 1
                if debounce_count >= DEBOUNCE_CUTOFF:
                    # Switch to day
                    current_state = "day"
                    debounce_count = 0
                    await send_new_state()
            else:
                debounce_count = 0

# Socket receive helper (blocking)

def receive_from_socket():
    # Receives data and the sender's address
    # Buffer size is in bytes (application buffer, max size of data)
    # Only reads a single datagram (packet)
    # Before this function, packet is stored in the OS kernel receive buffer, which can hold multiple packets
    data, addr = sock.recvfrom(bufferSize)
    data_decoded = data.decode('utf-8')

    sock.sendto("RPi received OK".encode('utf-8'), addr)

    return data_decoded, addr

def init():
    # Allows multiple processes or threads to bind to this same IP
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    # Allows the socket to send and receive broadcast messages (blocked by default)
    # sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # Establishing the port that we will use to send and receive data on the localhost
    sock.bind(('', localPort))
    print(f"UDP server : {get_ip_address()}:{localPort}")

async def main():
    print("Server starting")

    server = await websockets.serve(handler, "127.0.0.1", 8767)

    print("Started server, port 8767")

    await forward_light_values()

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Google's public DNS server
    # Able to convert any name into an IP address
    s.connect(("8.8.8.8", 80))
    # Returns [IP address, port]
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address

if __name__ == '__main__':
    init()
    asyncio.run(main())