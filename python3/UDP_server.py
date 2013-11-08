import socket
import serial
import threading
import time
from Byte_Queue import Byte_Queue

UDP_IP = "10.0.0.12"
UDP_PORT = 5005

# initialize serial port
ser = serial.Serial('/dev/ttyACM0', 57600, timeout=None)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


def main():
    send_thread().start()
    recv_thread().start()


class send_thread( threading.Thread ):

    def run( self ):
        while True:
            MESSAGE = bytearray()
            c = bytearray()
            c.append(0)
            payload_length = bytearray()
            while c[0] != 254:
                c = ser.read(1)

            payload_length = ser.read(1)
            MESSAGE.append( c[0] )
            MESSAGE.append( payload_length[0] )

            remainder = ser.read(payload_length[0] + 6)
            for x in remainder:
                MESSAGE.append(x)

            sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
            # print("Sent Message.")


class recv_thread( threading.Thread ):
    def run( self ):
        byte_queue = Byte_Queue() # basic, no-frills queue implementation
        reply = sock.recv(256)      # get first chunk          

        for byte in reply:          # put all bytes into queue
            byte_queue.put(byte)     
        while True:
            message = bytearray()                  
            current = byte_queue.get() # get first byte
            while current != 254:      # while not start byte 
                if byte_queue.empty():   # if empty, get more data from socket
                    reply = sock.recv(256)
                    for byte in reply:   # and put it into queue
                        byte_queue.put(byte)
                current = byte_queue.get()
            message.append(current) # append start byte
            current = byte_queue.get() # get payload length
            message.append(current) # append payload length
            for x in range(0, current + 6):  # get remaining message bytes from queue
                if byte_queue.empty():
                    reply = sock.recv(256)
                    for byte in reply:
                        byte_queue.put(byte)
                message.append(byte_queue.get())  # append bytes to message
            ser.write(message)        # write to the serial port
             

if __name__ == "__main__":
    main()
