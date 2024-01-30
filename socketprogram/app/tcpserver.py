import socket
import hashlib
import time

# Server details
HOST = "server"
PORT = 8000

# Create a TCP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Bind the socket to the specified address and port
    s.bind((HOST, PORT))
    # Listen for incoming connections
    s.listen()
    
    # Accept a connection from a client
    conn, addr = s.accept()

    # Connection established, print client information
    with conn:
        print(f"Connected by {addr}")

        # Infinite loop to continuously receive data from the client
        while True:
            # Receive data from the client (file number in this case)
            data = conn.recv(1024)

            # Check if there is no more data (client disconnected)
            if not data:
                break

            # Decode the received data (file number in string format)
            file_num_in_string = data.decode()

            # Sending small object
            small_filepath = '/root/objects/small-' + file_num_in_string + '.obj'
            small_md5_path = small_filepath + '.md5'

            print(f"Sending small file at {small_filepath}")
            print(f"Sending small object number: {file_num_in_string}")

            # Read the content of the small file
            with open(small_filepath, 'rb') as f:
                small_file_data = f.read()

            # Determine the length of the size string
            x = len(str(len(small_file_data)))
            if x > 9:
                print("deneme1")
                conn.send(str(x).encode())
            else:
                print("deneme2")
                y = 0
                z = str(y) + str(x)
                conn.send(z.encode())

            # Send the size of the small file
            small_file_size = str(len(small_file_data)).encode()
            conn.send(small_file_size)
            print(f"Small file size sent: {len(small_file_data)} bytes")

            # Read the MD5 hash of the small file
            with open(small_md5_path, 'r') as f:
                small_md5_hash = f.read()

            # Send the MD5 hash of the small file
            conn.send(small_md5_hash.encode())
            print(f"Small MD5 hash sent: {small_md5_hash}")

            # Record the start time for sending the small packet
            start_time_small = time.time()
            # Send the content of the small file
            conn.sendall(small_file_data)
            # Record the end time for sending the small packet
            end_time_small = time.time()
            print(f"Small file data sent")

            # Calculate and print the time taken to send the small packet
            elapsed_time_small = end_time_small - start_time_small
            print(f"Time taken to send small packet: {elapsed_time_small} seconds")

            # Write the time to the small-times.txt file
            with open("small-times.txt", 'a') as time_file:
                time_file.write(f"{file_num_in_string}: {elapsed_time_small} seconds\n")

            # Sending large object
            large_filepath = '/root/objects/large-' + file_num_in_string + '.obj'
            large_md5_path = large_filepath + '.md5'

            print(f"Sending large file at {large_filepath}")
            print(f"Sending large object number: {file_num_in_string}")

            # Read the content of the large file
            with open(large_filepath, 'rb') as f:
                large_file_data = f.read()

            # Determine the length of the size string
            x = len(str(len(large_file_data)))
            if x > 9:
                conn.send(str(x).encode())
            else:
                y = 0
                z = str(y) + str(x)
                conn.send(z.encode())

            # Send the size of the large file
            large_file_size = str(len(large_file_data)).encode()
            conn.send(large_file_size)
            print(f"Large file size sent: {len(large_file_data)} bytes")

            # Read the MD5 hash of the large file
            with open(large_md5_path, 'r') as f:
                large_md5_hash = f.read()

            # Send the MD5 hash of the large file
            conn.send(large_md5_hash.encode())
            print(f"Large MD5 hash sent: {large_md5_hash}")

            # Record the start time for sending the large packet
            start_time_large = time.time()
            # Send the content of the large file
            conn.sendall(large_file_data)
            # Record the end time for sending the large packet
            end_time_large = time.time()
            print(f"Large file data sent")

            # Calculate and print the time taken to send the large packet
            elapsed_time_large = end_time_large - start_time_large
            print(f"Time taken to send large packet: {elapsed_time_large} seconds")

            # Write the time to the large-times.txt file
            with open("large-times.txt", 'a') as time_file:
                time_file.write(f"{file_num_in_string}: {elapsed_time_large} seconds\n")

