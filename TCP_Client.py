import socket
import pyDes
import random
import time
import json
from datetime import datetime

def nickname():
    with open('username.txt', 'r') as f:
        your_last_name = json.load(f)

    print(f"Your last name is \'{your_last_name}\'")
    answer = input("Do you want to keep your last name? (y/n): ")
    if answer.lower() == "n":
        your_name = input("Enter a name: ")
        with open('username.txt', 'w') as f:
            json.dump(your_name, f)
    elif answer.lower() == "y":
        your_name = your_last_name
    else:
        print("Invalid input, your last name will remain the same.")
        your_name = your_last_name
    return your_name

def ask_user(users):

    print("Active users:\n")
    local_ip = socket.gethostbyname(socket.gethostname())
    while True:
        for username in users:
            ip_address_compare = users[username][0]
            if local_ip == ip_address_compare:
                print(username + " (Online) (me)")
            else:
                print(username + " (Online)")
        

        if not users:
            print("No active users\n")
            time.sleep(2)
            return

        username = input("\nEnter the username of the user you want to send a message to: ")
        if username not in users:
            print("User not found")
            time.sleep(2)
            continue
        else:
            break
    
    ip_address = users[username][0]

    return ip_address

def get_diffie_hellman_choice(sock):
    while True:
        # Ask the user if they want to use Diffie-Hellman encryption
        use_diffie_hellman = input("Do you want to use Diffie-Hellman encryption? (y/n): ")
        
        if not use_diffie_hellman == "y":
            if not use_diffie_hellman == "n":
                print("Invalid input, please try again.")
                continue 
        
        use_diffie_hellman1 = json.dumps({"choice": use_diffie_hellman.lower()})
        sock.send(use_diffie_hellman1.encode())

        return use_diffie_hellman

def diffie_hellman(sock):
    # Generate a shared secret key using the Diffie-Hellman key exchange algorithm
    base = 5
    modulus = 23
    private_key = random.randint(1, modulus)

    # Send the public key to the client
    public_key = (base ** private_key) % modulus
    public_key = json.dumps({"key": public_key})
    sock.send(public_key.encode())

    # Receive the public key from the client
    other_public_key = sock.recv(1024)
    other_public_key= json.loads(other_public_key.decode())
    other_public_key = other_public_key["key"]

    shared_secret_key = (other_public_key ** private_key) % modulus
    return shared_secret_key

def message_encrypt_send(sock, shared_secret_key, message):
    # Encrypt the message with the shared secret key
    key = str(shared_secret_key).rjust(8, '0')
    des = pyDes.des(key, pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
    encrypted_message = des.encrypt(message.encode('utf-8'))

    encrypted_message = list(encrypted_message) # It woooorks

    # Send the encrypted message in JSON format    
    encrypted_message = json.dumps({"encrypted_message": encrypted_message})
    sock.send(encrypted_message.encode())
    message_sent_time =Get_Time()

    return message_sent_time

def message_no_encrypt_send(sock, message):
    # Send the message without encryption
    message = json.dumps({"message": message})
    sock.send(message.encode())
    message_sent_time =Get_Time()

    return message_sent_time

def Save_Chat(username, message_unchanged, message_sent_time):
    message = f"Me to {username}: {message_unchanged}"

    with open('Chat_History.txt', 'a', encoding='utf-8') as f:
        f.write(message.ljust(100) + " " + message_sent_time + "\n")

def Get_Time():
    # Get the current date and time
    now = datetime.now()
    # Convert the date and time to a string
    message_receive_time = now.strftime("%Y-%m-%d %H:%M:%S")

    return message_receive_time

def close_socket(sock):
    sock.close()
    time.sleep(2)

def Chat_Initiator():
    loop = 3

    while loop == 3:
        print("""
****************************************
    Welcome to the chat application!
        
        1. See chat history
        2. Send message
        
    Type 'EXIT' to exit the chat
****************************************
        """)

        choice = input("Enter your choice: ")
        if choice == "1":
            print("\n")
            with open('Chat_History.txt', 'r', encoding='utf-8') as f:
                print(f.read())
            while True:
                choice = input("Press 'ENTER' to return to the main menu: ")
                if choice == "":
                    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
                    break
                else:
                    continue
            continue

        elif choice == "2":
            pass

        elif choice == "EXIT":
            print("Closing the application...")
            time.sleep(2)
            break

        else:
            print("Invalid input, please try again.")
            time.sleep(2)
            continue

        # Create a TCP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            your_name = nickname()

            # The dictionary of users and their IP addresses
            with open('active_users.txt', 'r') as f:
                users = json.loads(f.read())

            ip_address = ask_user(users)

            # Connect to the user's IP address
            sock.connect((ip_address, 6001))
            
            use_diffie_hellman = get_diffie_hellman_choice(sock)

            shared_secret_key = diffie_hellman(sock) if use_diffie_hellman.lower() == "y" else None
            
            loop = 5
            while loop == 5:
                try:
                    # The message you want to send
                    message_unchanged = input("Your message: ")

                    if not message_unchanged:
                        print("Please enter a message")
                        continue

                    if message_unchanged == "EXIT":
                        print("Exiting the chat...")
                        close_socket(sock)
                        loop = 3
                        continue

                    message = f"{your_name}: {message_unchanged}"

                    message_sent_time = message_encrypt_send(sock, shared_secret_key, message) if use_diffie_hellman.lower() == "y" else message_no_encrypt_send(sock, message) 
                    
                    if ip_address == socket.gethostbyname(socket.gethostname()):
                        username = "myself"

                    Save_Chat(username, message_unchanged, message_sent_time)

                except ConnectionAbortedError:
                    print("The user has left the chat.")
                    loop = 1
                    sock.close()
                    time.sleep(2)
                    continue    
                
                except KeyboardInterrupt:
                    print("\nExiting the chat...")
                    loop = 0
                    close_socket(sock)

        except KeyboardInterrupt:
            print("\nClosing the Application...")
            close_socket(sock)
            break

        except ConnectionRefusedError:
            print("The user is not available.")
            loop = 1
            time.sleep(2)

        except Exception as err:
            print("This error happened: " + str(err))
            print("Please try again")
            time.sleep(1)

Chat_Initiator()