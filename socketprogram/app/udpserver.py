#udpserver.py
import hashlib
import socket
import threading
import time

# Server details
localIP     = "server"  # Change to your server IP
localPort   = 8000
bufferSize  = 1024

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")

# Global variables for managing acknowledgments and window
ack_received = []
window_size = 7
send_base = 0
packet_status = {}
last_packet_sent_time = {}  # Dictionary to store the last sent time for each packet
timeout_duration = 1.0

stop_thread = False

def restart_threads():
    global stop_thread, ack_thread, packet_status, last_packet_sent_time, timeout_duration
    stop_thread = False  # Reset the flag
    ack_thread = threading.Thread(target=ack_receiver)  # Recreate the thread
    ack_thread.daemon = True
    ack_thread.start()
    packet_status = {}
    last_packet_sent_time = {}  #
    timeout_duration = 1.0


# Function to reset global variables for next transfer
def reset_globals():
    global send_base, ack_received
    send_base = 0
    ack_received.clear()
# Function to handle multiple file transfers
def handle_multiple_transfers(filenames, clientAddr):
    for filename in filenames:
        print(f"Starting transfer for {filename}")
        reset_globals()  # Reset global variables for the next file (consider to put it below)
        UDP_sender(filename, clientAddr)  # Call your existing file transfer function


# Packet creation
def create_packet(seq, data):
    checksum = hashlib.md5(data.encode()).hexdigest()
    return f'{seq}:{checksum}:{data}'.encode()

# Send packet
def send_packet(packet, addr):
    UDPServerSocket.sendto(packet, addr)

# Receive acknowledgments
def ack_receiver():
    global send_base, packet_status, stop_thread
    while True:
        if stop_thread:
            break
        msg, _ = UDPServerSocket.recvfrom(bufferSize)
        try:
            ack_seq = int(msg.decode().split(':', 1)[0])
            if ack_seq >= send_base:
                ack_received.append(ack_seq)
                packet_status[ack_seq] = True
        except ValueError:
            # Handle messages that are not in the expected format
            print(f"Ignoring unexpected message: {msg}")
            continue


# UDP Sender function
def UDP_sender(filename, clientAddr):
    start_time = time.time()
    global send_base
    with open(filename, "r") as f:
        seq = 0
        packets_to_send = []

        # Read and packetize the entire file
        while True:
            data = f.read(bufferSize - len(str(seq)) - 32 - 2) ##????
            if not data:
                break
            packet = create_packet(seq, data)
            packets_to_send.append((seq, packet))
            last_packet_sent_time[seq] = -2
            packet_status[seq] = False
            seq += 1

        # Start sending packets
        # TODO Resending should be implemented
        # TODO In case of not having an ack received
        while send_base < seq:
            for seq_number in range(send_base, send_base + window_size):
                if seq_number < seq:
                    if not packet_status[seq_number]:
                        current_time = time.time()
                        if current_time - last_packet_sent_time[seq_number] > timeout_duration:
                            packet_seq, packet = packets_to_send[seq_number]
                            send_packet(packet, clientAddr)
                            #print(f"Sent packet {packet_seq}")
                            last_packet_sent_time[packet_seq] = current_time
                    elif seq_number == send_base and packet_status[seq_number] == True:
                        send_base += 1

            # If all packets are sent and acknowledged
            if send_base >= seq:
                break

            time.sleep(0.1)  # Adjust timing as needed for your network conditions

        # Send a final message indicating transfer completion
        send_packet(b'END', clientAddr)
        end_time = time.time()
        if 'md5' not in filename:
            print(f"{filename}, completed in {end_time - start_time} secs")
        elif 'large' in filename:
            print(f"{filename}, LARGE FILE completed in {end_time - start_time} secs")
        elif 'small' in filename:
            print(f"{filename}, LARGE FILE completed in {end_time - start_time} secs")

ack_thread = threading.Thread(target=ack_receiver)
ack_thread.daemon = True


while True:
    # Wait for an incoming connection
    print("Waiting for incoming connection...")
    data, addr = UDPServerSocket.recvfrom(bufferSize)

    if data.decode() == 'bye':
        break


    file_number = data.decode()
    print(f"Connection established with {addr}")
    large_file = '/root/objects/large-' + file_number + '.obj'
    small_file = '/root/objects/small-' + file_number + '.obj'
    file_list = [small_file, small_file + '.md5', large_file, large_file + '.md5']  # Add paths to your files
    # Start acknowledgment receiver thread
    restart_threads()
    handle_multiple_transfers(file_list, addr)
    stop_thread = True
