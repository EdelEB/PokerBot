import sys
import socket

#run command to run on loopback ip
#python3.10 client_player.py 127.0.0.1 1200

def get_ip():
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

# Read server IP address and port from command-line arguments
serverIP = get_ip()  # ip address "unused ports"?
serverPort = 12000

# Create a UDP socket. Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # necessary to send/receive data
# Assign server IP address and port number to socket
serverSocket.bind((serverIP, serverPort))

print("The server is ready to receive on port:  " + str(serverPort) + "\n")

# loop forever listening for incoming UDP messages
while True:
    # Receive and print the client data from "data" socket
    data, address = serverSocket.recvfrom(1024)  # 1024 upper bound of data size
    print(f"Receiving data from client {address[0]}, {address[1]}: {data.decode()}")

    # Echo back to client
    print(f"Sending data to client {address[0]}, {address[1]}: {data.decode()}")
    serverSocket.sendto(data, address)

# LoopBack IP 127.0.0.1
# both client and server using UDP