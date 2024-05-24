import socket
import json
import time

def auto_Broadcast_IP():
    # The broadcast IP and port
    ip = socket.gethostbyname(socket.gethostname())
    parts = ip.split('.')
    parts[-1] = '255'
    broadcast_ip = '.'.join(parts)
    return broadcast_ip
    
def Service_Announcer():
    # Ask for the username
    username = input("Enter your username: ")

    # Save the username to a file
    with open('username.txt', 'w') as f:
        json.dump(username, f)

    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set the broadcast option for the socket
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Get the broadcast IP and port
    broadcast_ip = auto_Broadcast_IP()
    broadcast_port = 6000

    print(f"Broadcasting the username: {username}")
    try:
        while True:
            # Create the message
            message = json.dumps({"username": username})

            # Send the message
            sock.sendto(message.encode(), (broadcast_ip, broadcast_port))

            # Wait for 8 seconds before sending the next broadcast
            time.sleep(8)
            
    except KeyboardInterrupt:
        print("\nService Announcer is shutting down...")
        sock.close()

Service_Announcer()