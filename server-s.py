import socket
import signal
import sys
import time

def signal_handler(signum, frame):
    global not_stopped
    not_stopped = False

def main():
    if len(sys.argv) != 2:
        sys.stderr.write("ERROR: Invalid number of arguments\n")
        sys.exit(1)

    port = int(sys.argv[1])

    # Handle signals
    signal.signal(signal.SIGQUIT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    # Create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Check if the port is within valid range (0-65535)
        if not (0 <= port <= 65535):
            sys.stderr.write("ERROR: Port must be within range 0-65535\n")
            sys.exit(1)

        # Bind to the specified IP and port
        server_socket.bind(('0.0.0.0', port))

        # Listen for incoming connections
        server_socket.listen(10)  # Maximum 10 pending connections

        not_stopped = True
        while not_stopped:
            try:
                # Accept a connection
                client_socket, client_address = server_socket.accept()
                print(f"Accepted connection from {client_address}")

                # Send "accio\r\n" command
                client_socket.send(b"accio\r\n")

                # Set a timeout for receiving data
                client_socket.settimeout(10)  # Adjust the timeout as needed

                # Receive data and count bytes
                total_bytes_received = 0
                while True:
                    data = client_socket.recv(4096)
                    if not data:
                        break
                    total_bytes_received += len(data)

                print(f"Received {total_bytes_received} bytes")

                # Close the connection
                client_socket.close()

            except socket.timeout:
                sys.stderr.write("ERROR: Connection timed out\n")
                continue

    except OSError as e:
        sys.stderr.write(f"ERROR: {str(e)}\n")
        sys.exit(1)

    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
