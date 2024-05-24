import socket
import json
import time

def clear_file(online_users):
    online_users.clear() # Clear the online users list
    with open('active_users.txt', 'w') as f:
        json.dump(online_users, f)

def Peer_Discovery():
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to the port 6000
    sock.bind(('', 6000))

    # A dictionary to store the active users
    active_users = {}
    online_users = {}

    sock.settimeout(5.0)  # Peer Discovery's period

    try:
        loop = 0
        while True:
            try:
                # Receive a message
                data, addr = sock.recvfrom(1024)

                # Decode the message
                message = json.loads(data.decode())

                active_users[message['username']] = (addr[0], time.time())

            except socket.timeout:
                pass # Do nothing if no message is received
            except Exception as err:
                print("This error happened: " + str(err))
                print("Please try again")
                continue
            
            # Check if there are active users
            if not active_users:
                if loop == 0:
                    loop = 1
                    continue
                print("\nNo active users")
            else:
                # Open the file in write mode
                with open('active_users.txt', 'w') as f:
                    print("\nUsers Current Status:")
                    # Check the status of each user
                    for username, (ip, last_heard) in list(active_users.items()):
                        # If we haven't heard from a user in more than 15 minutes, remove them from the list
                        if time.time() - last_heard > 900:
                            print(f"{username} (Offline)")
                            del active_users[username]
                        else:
                            # If we haven't heard from a user in more than 10 seconds, mark them as away
                            if time.time() - last_heard > 10: 
                                status = "(Away)" 
                                last_heard_minute= int((time.time() - last_heard) / 60)
                                print(f"{username} {status}, Last online: {last_heard_minute} minutes ago")
                            else: 
                                status = "(Online)"
                                print(f"{username} {status}")
                                online_users[username] = (ip, last_heard)
                            
                    # Write the dictionary to the file
                    with open('active_users.txt', 'w') as f:
                        json.dump(online_users, f)

    except KeyboardInterrupt:
        print("\nPeer Discovery is shutting down...")
        sock.close()
        clear_file(online_users)

    except Exception as err:
        print("This error happened: " + str(err))
        print("Please try again")
        sock.close()
        clear_file(online_users)

Peer_Discovery()