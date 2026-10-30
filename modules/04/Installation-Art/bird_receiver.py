import socket
import threading
import struct
import json
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

localPort = 8888
bufferSize = 1024

# String defining layout of data foo received packet
FMT = "<iif"                      # int32 bird_id, int32 branch, float32 volume
SIZE = struct.calcsize(FMT)       # 12 bytes

# Dictionary for keeping track of birds
birds = {}                        # bird_id -> {"branch", "volume", "updated"}
birds_lock = threading.Lock()

# AF_INET - Address family IPv4, meaning that socket will use 4-part IP address
# SOCK_DGRAM = Socket type is Datagram (UDP instead of TCP)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def init():

    # Let's multiple sockets share port (probably not necessary)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.bind(('', localPort)) # Binds
    print(f"UDP server : {get_ip_address()}:{localPort}")

# Loop for receiving, parsing, and sorting state of birds
def receive_loop():
    while True:
        # Waits until one UDP packet arrives on the socket, then returns that packet’s contents and sender’s address.
        data, addr = sock.recvfrom(bufferSize) 


         # Ignore malformed packets
        if len(data) != SIZE:
            continue
        
        # Parse received data. 
        # Struct.unpack() turns data in primitive python data types using FMT, a string defining expected layout of data
        bird_id, branch, volume = struct.unpack(FMT, data)
        print(bird_id, branch, volume)
        # Wait until aquire lock then edit state
        with birds_lock:
            birds[bird_id] = {
                "branch": branch,
                "volume": volume,
            }

        # Send confirmation of package reception back to esp
        sock.sendto(b"RPi received OK", addr)

# Class for 
class BirdHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Make sure get request is asking for birds' states
        if self.path != "/birds":
            self.send_error(404)
            return

        # Aquire lock then create response to request
        with birds_lock:
            # Converts dictionary to JSON string and encodes it into bytes
            response = json.dumps(birds).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))                # no packet is sent; just picks a route
        return s.getsockname()[0]
    except OSError:
        return "unknown"
    finally:
        s.close()


if __name__ == '__main__':
    init()
    # Create thread for function that receives data from esp and updates state
    threading.Thread(target=receive_loop, daemon=True).start()

    # Main thread for creating http server 
    server = ThreadingHTTPServer(("127.0.0.1", 8080), BirdHandler)
    print("HTTP server at http://127.0.0.1:8080/birds")
    server.serve_forever()