import socket
import random

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
print(ip_address)

# Bind the socket to a specific address and port
server_socket.bind((ip_address, 5000))

expected_sequence_number = 0
received_sequence_numbers = set()

while True:
    # Receive a message from the client
    message, client_address = server_socket.recvfrom(1024)
    print('Received message from {}: {}'.format(client_address, message.decode()))

    # Extract the sequence number from the message
    try:
        sequence_number = int(message.decode().split()[1])
    except ValueError:
        # Invalid message, ignore
        continue

    if sequence_number == expected_sequence_number:
        # If the received sequence number is the expected sequence number, send an ACK and move to the next sequence number
        expected_sequence_number += 1
        ack = "ACK {}".format(expected_sequence_number).encode()
        server_socket.sendto(ack, client_address)
        print('Sent ACK {} to {}.'.format(expected_sequence_number, client_address))
    elif sequence_number in received_sequence_numbers:
        # If the received sequence number has been seen before, send the same ACK again
        ack = "ACK {}".format(sequence_number+1).encode()
        server_socket.sendto(ack, client_address)
        print('Sent duplicate ACK {} to {}.'.format(sequence_number+1, client_address))
    else:
        # If the received sequence number is not the expected sequence number and has not been seen before, don't send an ACK
        print('Received out-of-order packet from {}.'.format(client_address))

    received_sequence_numbers.add(sequence_number)

    # Generate random number to simulate packet loss
    rand = random.randint(1, 10)

    if rand > 5:  # Simulate packet loss
        # Don't send response, wait for retransmission
        print('Simulating packet loss.')
    else:
        # Send response as usual
        server_socket.sendto(message, client_address)
        print('Sent message back to {}.'.format(client_address))

    # Check if the end of communication has been reached
    if message.decode().split()[0] == "END":
        print('End of communication reached, closing connection.')
        server_socket.close()
        break