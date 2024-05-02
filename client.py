import socket

host = "192.168.56.1"  # Change this to the IP address where your server is running
port = 7777

s = socket.socket()
s.connect((host, port))

# Receive the banner
data = s.recv(1024)
# Print the banner
print(data.decode().strip())

# Get difficulty choice from the user
difficulty_choice = input("Enter difficulty choice (a, b, c): ").strip().lower()
s.sendall(difficulty_choice.encode())

while True:
    # Receive the banner
    data = s.recv(1024)
    # Print the banner
    print(data.decode().strip())
    

    # Get input from the user
    user_input = input("").strip()

    s.sendall(user_input.encode())
    reply = s.recv(1024).decode().strip()
    print(reply)
    if "Correct" in reply:
        # Prompt for retry
        retry_input = input().strip().lower()
        s.sendall(retry_input.encode())
        if retry_input != 'y':
            if retry_input == 'n':
                print("Thanks for Playing!")
            break

s.close()
