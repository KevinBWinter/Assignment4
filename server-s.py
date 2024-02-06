import socket
import signal
import sys

# Define a global flag to control server loop execution
not_stopped = True

def signal_handler(signum, frame):
    global not_stopped
    not_stopped = False
    print("Signal received, shutting down the server...")

def handle_client(client_socket):
    try:
        client_socket.send(b"Welcome\r\n")
        client_socket.settimeout(10)  # Set timeout for receiving data

        total_bytes_received = 0
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            total_bytes_received += len(data)

        print(f"Received {total_bytes_received} bytes from {client_socket.getpeername()}")

    except socket.timeout:
        print("ERROR: Connection timed out")
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        client_socket.close()

def main():
    if len(sys.argv) != 2:
        print("ERROR: Invalid number of arguments. Usage: python script.py <PORT>")
        sys.exit(1)

    port = int(sys.argv[1])
    if not (0 <= port <= 65535):
        print("ERROR: Port must be within range 0-65535")
        sys.exit(1)

    # Setup signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('0.0.0.0', port))
        server_socket.listen()

        print(f"Server listening on port {port}")

        while not_stopped:
            try:
                server_socket.settimeout(1)  # Check for shutdown signal
                client_socket, addr = server_socket.accept()
            except socket.timeout:
                continue  # Go back to the top of the loop to check not_stopped flag

            print(f"Accepted connection from {addr}")
            # Using threading to handle each client connection
            threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    main()
