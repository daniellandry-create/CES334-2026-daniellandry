import serial
import time

HEADER_BYTE = 0xAA
FRAME_LEN = 4

class Controller:
    
    def __init__(self, port='/dev/ttyUSB0',baud=115200):

        self.ser = serial.Serial(port, baud, timeout=0)

        # clear input buffer 
        self.ser.reset_input_buffer()

        self.buffer = b""

        self.state = 0

        self.last_valid = time.monotonic()
        

    def update(self):
        
        # Save bytes in serial buffer to class buffer
        self.buffer += self.ser.read(self.ser.in_waiting)

        *lines, self.buffer = self.buffer.split(b"\n")

        for line in reversed(lines):
            try:
                value = int(line.strip()) # Remove all leading and trailing whitespace
            except ValueError:  # built-in exception raised when a function or operation receives an argument that has the correct data type but an inappropriate or invalid value
                continue                  # Garbled line, try an older one
            if 0 <= value <= 0xFFFF: # If good value, mark time
                self.state = value
                self.last_valid = time.monotonic()
                break

        #if time.monotonic() - self.last_valid > 0.2:
            #self.state = 0

    def is_pressed(self, bit):
        return ((self.state & (1 << bit)) > 0)


