import socket
import sys
import time

# Check if the number of arguments is correct
if len(sys.argv) != 3:
    print("Usage: UDP_ping_Client.py <number_of_pings> <server_IP_address>")
    sys.exit()

# Get the number of pings to send and server IP address from the command line arguments
num_pings = int(sys.argv[1])
server_ip = sys.argv[2]

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(5)  # Set timeout to 1 second

# Initialize variables for statistics
rtt_times = []
lost_packets = 0

# Send the ping messages to the server
for i in range(num_pings):
    # Send the ping message
    message = "Ping " + str(i+1) + " " + str(time.time())
    start_time = time.time()
    client_socket.sendto(message.encode(), (server_ip, 5000))

    try:
        # Receive the response from the server
        response, server_address = client_socket.recvfrom(1024)
        end_time = time.time()

        # Calculate the round-trip time
        rtt = (end_time - start_time) * 1000  # in milliseconds
        rtt_times.append(rtt)

        # Print the response message
        print("Received response from {}: {}".format(server_address, response.decode()))
        print("Round-trip time: {:.3f} ms\n".format(rtt))
    except socket.timeout:
        # The packet was lost
        print("Request timed out.\n")
        lost_packets += 1

# Print statistics
print("--- Ping statistics ---")
print("{} packets transmitted, {} packets received, {:.2f}% packet loss".format(num_pings, num_pings - lost_packets, (lost_packets/num_pings)*100))
if rtt_times:
    print("round-trip min/avg/max/stddev = {:.3f}/{:.3f}/{:.3f}/{:.3f} ms".format(min(rtt_times), sum(rtt_times)/len(rtt_times), max(rtt_times), ((sum((x - sum(rtt_times)/len(rtt_times))**2 for x in rtt_times))/len(rtt_times))**0.5))

# Close the socket
client_socket.close()