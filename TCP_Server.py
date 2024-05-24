import socket
import json
import pyDes
import time
import random
from datetime import datetime

def diffie_hellman(conn):
    # Generate a shared secret key using the Diffie-Hellman key exchange algorithm
    base = 5
    modulus = 23
    private_key = random.randint(1, modulus)
    public_key = (base ** private_key) % modulus
    
    # Receive the public key from the client
    other_public_key = conn.recv(1024)
    other_public_key= json.loads(other_public_key.decode())
    other_public_key = other_public_key["key"]
    
    # Send the public key to the client
    public_key = json.dumps({"key": public_key})
    conn.send(public_key.encode())

    shared_secret_key = (other_public_key ** private_key) % modulus
    return shared_secret_key

def Get_Time():
    # Get the current date and time
    now = datetime.now()
    # Convert the date and time to a string
    message_receive_time = now.strftime("%Y-%m-%d %H:%M:%S")

    return message_receive_time

def diffie_hellman_bool(conn):
    # Receive the choice of encryption from the client
    diffie_hellman_choice = conn.recv(1024).decode() 
    diffie_hellman_choice = json.loads(diffie_hellman_choice)
    diffie_hellman_choice = diffie_hellman_choice["choice"]

    return diffie_hellman_choice

def message_decrypt(conn, shared_secret_key):
    # Receive the encrypted message
    encrypted_message = conn.recv(1024)
    message_receive_time = Get_Time()
    encrypted_message = json.loads(encrypted_message.decode())
    encrypted_message = bytes(encrypted_message["encrypted_message"]) # WoaW

    # Decrypt the message with the shared secret key
    key = str(shared_secret_key).rjust(8, '0')
    des = pyDes.des(key, pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
    message = des.decrypt(encrypted_message)
    message = message.decode('utf-8')

    # Print the decrypted message
    print(message.ljust(100) + " " + message_receive_time)

    return message, message_receive_time

def message_no_decrypt(conn):
    message = conn.recv(1024).decode()
    message_receive_time = Get_Time()
    message = json.loads(message)
    message = message["message"]

    # Print the message
    print(message.ljust(100) + " " + message_receive_time)

    return message, message_receive_time

def Chat_Responder():
    # Create a TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_ip = socket.gethostbyname(socket.gethostname())

    # Bind the socket to a specific address and port
    sock.bind((client_ip, 6001))  # Replace with your actual IP address and port number

    sock.listen(1)

    loop = 1
    while True:
        print("Listening for incoming connections...")

        socket.setdefaulttimeout(10.0)  # Chat Responder's period
        try:
            # Accept a connection
            conn, addr = sock.accept()
            print("Connection established\n")

            diffie_hellman_choice = diffie_hellman_bool(conn)
            
            if diffie_hellman_choice == "y":  # Use Diffie-Hellman encryption
                shared_secret_key = diffie_hellman(conn)

            loop = 2
            socket.setdefaulttimeout(5.0)  # Chat Responder's period
            while loop == 2:
                try:
                    
                    message, message_receive_time = message_decrypt(conn, shared_secret_key) if diffie_hellman_choice == "y" else message_no_decrypt(conn) # Use Diffie-Hellman encryption

                    if not addr[0] == client_ip:
                        # Save the message to a file
                        with open('Chat_History.txt', 'a', encoding='utf-8') as f:
                            f.write(message.ljust(100) + " " + message_receive_time + "\n")
                
                except socket.timeout:
                    continue

                except UnicodeError:
                    print("Please use UTF-8 encoding for your message")
                    continue

                except socket.error as e:
                    if isinstance(e, ConnectionResetError):
                        print("Connection closed by the client\n")
                        conn.close()
                        loop = 1
                        break
                    if isinstance(e, ConnectionAbortedError):
                        print("Connection closed by the client\n")
                        conn.close()
                        loop = 1
                        break
                      
                except json.decoder.JSONDecodeError:
                    print("Connection closed by the client\n")
                    conn.close()
                    loop = 1
                    continue

                except:
                    print("Connection error...\n")
                    conn.close()
                    loop = 1
                    break

        except KeyboardInterrupt:
            print("\nServer is shutting down...")
            try:
                conn.close()
            except:
                pass
            sock.close()
            time.sleep(2)
            return
        
        except socket.timeout:
            continue
        
        except WindowsError:
            print("Client is forcibly closed...\n")
            continue

        except Exception as err:
            print("This error happened: " + str(err))
            print("Please try again")
            continue
       

Chat_Responder()