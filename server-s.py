import socket
import signal
import sys
import threading

# Define a global flag to control server loop execution
not_stopped = True

def signal_handler(signum, frame):
    global not_stopped
    not_stopped = False
    print("Signal received, shutting down the server...")

def handle_client(client_socket):
    try:
        client_socket.send(b"accio\r\n")  # Sending initial data to the client
        client_socket.settimeout(10)  # Set timeout for receiving data

        total_bytes_received = 0
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            total_bytes_received += len(data)

        print(f"Received {total_bytes_received} bytes")

    except socket.timeout:
        print("ERROR: Connection timed out")
    except Exception as e:
        print(f"ERROR: {str(e)}")
    finally:
        client_socket.close()

def accept_connections(server_socket):
    while not_stopped:
        try:
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}")
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()
        except Exception as e:
            if not_stopped:  # Only log errors if not stopping
                print(f"Error accepting connection: {e}")

def main():
    global not_stopped

    if len(sys.argv) != 2:
        print("ERROR
