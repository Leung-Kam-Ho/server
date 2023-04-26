
import cv2
import socket
import pickle
import struct
import threading
import time

class Server:
    # create a socket object
    def __init__(self) -> None:
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.quit = False
        # get local machine name
        host = socket.gethostname()
        
        #host = "192.168.2.2"
        #host = "192.168.2.1"
        port = 9999

        # bind the socket to a public host, and a well-known port
        self.serversocket.bind((host, port))

        # become a server socket
        self.serversocket.listen(1)
        self.cap = cv2.VideoCapture(0)
        print("Waiting for incoming connections...")

        
    def connect(self):
        # establish a connection
        self.clientsocket, self.addr = self.serversocket.accept()
    def Send(self):
        print("Got a connection from %s" % str(self.addr))
        # create a VideoCapture object to capture frames from the webcam or video file
        
        msg = {}
        while not s.quit:
            # read a frame from the VideoCapture object
            ret, frame = self.cap.read()
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
            _, img_encoded = cv2.imencode('.jpg', frame, encode_param)
            msg["frame"] = img_encoded
            msg["msg"] = "hi"
            # encode the frame into a format that can be sent over the network
            data = pickle.dumps(msg,0)
            message_size = struct.pack("<L", len(data))
            
            # send the size of the message first
            try:
                self.clientsocket.send(message_size)
                # send the actual message
                self.clientsocket.sendall(data)
            except KeyboardInterrupt:
                self.quit = True
                break
            except:
                break
        print("SOMETHING Wrong")
        # close the connection
        self.clientsocket.close()
            
        
                
        
    def Receive(self):
        while not self.quit:
                received = self.clientsocket.recv(1024).decode("ascii")
                
                rd = received.split(":")
                print(rd[0],rd[1])
                if received == "quit":
                    self.quit = True
                    break

    def close(self):
        self.serversocket.close()
if __name__ == "__main__":
    
    s = Server()
    
    
    while not s.quit:
        s.connect()
        rx = threading.Thread(target=s.Receive)
        rx.start()
        s.Send()

