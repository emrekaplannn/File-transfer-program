import socket
import hashlib
import time

# Server details
HOST = socket.gethostbyname("server")
PORT = 8000

# Create a client socket and connect to the server
client_socket = socket.socket()
client_socket.connect((HOST, PORT))

# Get the file number from the user
file_number = input("Enter file number (or 'bye' to exit): ")

# Main loop to interact with the server
while file_number.lower().strip() != 'bye':
    # Send the file number to the server
    client_socket.send(file_number.encode())

    # Receive and process small object
    small_file_size_size = client_socket.recv(2).decode()
    if small_file_size_size[0] == '0':
        a = int(small_file_size_size[1])
    else:
        a = int(small_file_size_size)

    small_file_size = int(client_socket.recv(a).decode())

    print(f"Received small file size: {small_file_size}")

    small_received_hash = client_socket.recv(33).decode().strip()
    small_file_data = b""
    while len(small_file_data) < small_file_size:
        chunk = client_socket.recv(1024)
        if not chunk:
            break
        small_file_data += chunk

    print(f"Small file {file_number} received but not checked for integrity")

    # Calculate MD5 hash for integrity check
    small_calculated_hash = hashlib.md5(small_file_data).hexdigest()
    print(f"Calculated md5 hash for small file: {small_calculated_hash}")

    # Check integrity and process accordingly
    if small_calculated_hash != small_received_hash:
        print(f"Small file {file_number} integrity check failed")
    else:
        print(f"Small file {file_number} received successfully")

        # Save the received small file_data to a file
        small_received_filename = f"received-small-{file_number}.obj"
        with open(small_received_filename, 'wb') as small_received_file:
            small_received_file.write(small_file_data)
            print(f"Small file {file_number} saved as {small_received_filename}")

    # Receive and process large object
    large_file_size_size = client_socket.recv(2).decode()
    if large_file_size_size[0] == '0':
        a = int(large_file_size_size[1])
    else:
        a = int(large_file_size_size)

    large_file_size = int(client_socket.recv(a).decode())

    print(f"Received large file size: {large_file_size}")

    large_received_hash = client_socket.recv(33).decode().strip()
    large_file_data = b""
    while len(large_file_data) < large_file_size:
        chunk = client_socket.recv(1024)
        if not chunk:
            break
        large_file_data += chunk

    print(f"Large file {file_number} received but not checked for integrity")

    # Calculate MD5 hash for integrity check
    large_calculated_hash = hashlib.md5(large_file_data).hexdigest()
    print(f"Calculated md5 hash for large file: {large_calculated_hash}")

    # Check integrity and process accordingly
    if large_calculated_hash != large_received_hash:
        print(f"Large file {file_number} integrity check failed")
    else:
        print(f"Large file {file_number} received successfully")

        # Save the received large file_data to a file
        large_received_filename = f"received-large-{file_number}.obj"
        with open(large_received_filename, 'wb') as large_received_file:
            large_received_file.write(large_file_data)
            print(f"Large file {file_number} saved as {large_received_filename}")

    # Get the next file number from the user
    file_number = input("Enter file number (or 'bye' to exit): ")

# Close the client socket when the loop exits
client_socket.close()

