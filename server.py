import socket
import subprocess
import os
import platform

def handle_client(client_socket):
    try:
        client_socket.send(b"Your unique key: Rtos4zCyPkl9s9gi\n")
        client_socket.send(b"Welcome to the Secure Shell server!\n")

        while True:
            client_socket.send(b" ")
            command = client_socket.recv(1024).decode().strip()

            # Checking for exit command
            if command == 'exit':
                client_socket.send(b"Goodbye!\n")
                break

            # Process the commands
            if command == 'status':
                client_socket.send(f"Server is running. Your unique key: Rtos4zCyPkl9s9gi\n".encode())
            
            elif command == 'dir':
                # Check for OS and run appropriate command
                if platform.system() == 'Windows':
                    command_output = subprocess.run('dir', shell=True, capture_output=True, text=True)
                else:
                    command_output = subprocess.run('ls', shell=True, capture_output=True, text=True)

                client_socket.send(command_output.stdout.encode())
            
            elif command.startswith('cat '):
                filename = command.split(' ')[1]
                try:
                    with open(filename, 'r') as file:
                        content = file.read()
                    client_socket.send(content.encode())
                except Exception as e:
                    client_socket.send(f"Error: {e}".encode())
            
            elif command.startswith('exec '):
                exec_command = command.split(' ', 1)[1]
                try:
                    # Execute the system command and return the result
                    exec_output = subprocess.run(exec_command, shell=True, capture_output=True, text=True)
                    if exec_output.stdout:
                        client_socket.send(exec_output.stdout.encode())
                    if exec_output.stderr:
                        client_socket.send(f"Error: {exec_output.stderr}".encode())
                except Exception as e:
                    client_socket.send(f"Error: {str(e)}".encode())

            else:
                client_socket.send(b"Unknown command.\n")
        
        client_socket.close()

    except Exception as e:
        print(f"Error: {e}")
        client_socket.send(b"Error occurred while processing your request.\n")
    finally:
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9999))
    server.listen(5)
    print("Server listening on port 9999...")
    
    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr[0]}:{addr[1]} has been established!")
        handle_client(client_socket)

start_server()
