import socket
import asyncio
import os
import json
import tempfile


localPort = 8888
bufferSize = 1024

# AF_INET - Address family IPv4, meaning that socket will use 4-part IP address
# SOCK_DGRAM = Socket type is Datagram (UDP instead of TCP)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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

    while True:
        data_encoded, addr = receive_from_socket()
        print(f'Data: {data_encoded}, From: {addr}')

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