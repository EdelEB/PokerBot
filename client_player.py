import socket

class Client_Player():
    def __init__(self, port):
        # Get the server hostname, port and data length as command line arguments
        self.HOST_IP = self.get_ip();  # ip address
        self.SERVER_IP = self.HOST_IP;
        self.SERVER_PORT = 1200;
        self.MESSAGE_SIZE = 1024;
        self.PORT = port;
        self.attempts = 0
        # Create UDP client socket. Note the use of SOCK_DGRAM
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __del__(self):
        # Close the client socket
        self.clientsocket.close()
        print("closed");

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip

    def send(self, data):
        # throws TimeoutError after one second
        self.clientsocket.settimeout(1)

        while self.attempts < 3:
            # Send data to server
            #print(f"Sending data to {self.host}, {self.port}: {data}")
            data = input(f"Send Message: ");
            if data == "end": break;

            self.clientsocket.sendto(data.encode(), (self.SERVER_IP, self.SERVER_PORT))
            try:
                # Receive the server response
                dataEcho, address = self.clientsocket.recvfrom(self.MESSAGE_SIZE)
                print(f"Received data from {address[0]}, {address[1]} : {dataEcho.decode()}")
                # break
            except:
                print("Error connecting to server \nretrying...")
                self.attempts += 1
        if self.attempts == 3:
            print("Could not connect to game \nPlease try again later\n")

def test():
    c = Client_Player(1200);

    print(c.HOST_IP)

    c.send("hello")

test();