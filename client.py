import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 9999))  # Connect to the server

    unique_key = client_socket.recv(1024).decode()
    print(f"Your unique key: {unique_key}")
    
    while True:
        # Ask user to input command
        command = input("Enter command: ")

        if command == 'exit':
            client_socket.send(command.encode())
            print("Goodbye!")
            break
        
        # Send the command to the server
        client_socket.send(command.encode())
        
        # Wait for prompt to press Enter
        print("Press Enter to see result...")

        # Wait for the user to press Enter
        input()

        # Receive the output from the server
        result = client_socket.recv(4096).decode()

        # Display the result after pressing Enter
        print(result)

    client_socket.close()

start_client()
