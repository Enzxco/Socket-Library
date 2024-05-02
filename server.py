import socket
import random
import os

# Define the host and port for the server
host = "0.0.0.0"
port = 7777

# Banner message to be sent to clients
banner = """
== Guessing Game v1.0 ==
Enter your name:"""

# Function to generate a random integer within a specified range
def generate_random_int(low, high):
    return random.randint(low, high)

# Initialize the socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

print(f"Server is listening on port {port}")

# Create directories to store leaderboard files if they don't exist
leaderboard_directory = "leaderboards"
if not os.path.exists(leaderboard_directory):
    os.makedirs(leaderboard_directory)

# Define the leaderboard dictionary to store user scores
leaderboard = {}

# Main server loop
while True:
    # Accept a new connection
    conn, addr = s.accept()
    print(f"New client connected: {addr[0]}")
    conn.sendall(banner.encode())  # Send the banner message to the client

    # Ask for user's name
    client_input = conn.recv(1024)
    name = client_input.decode().strip()

    # Send difficulty selection banner
    conn.sendall(b"""
Difficulty Level
1. Beginner (1-50)
2. Intermediate (1-100)
3. Challenger (1-500)
Enter the difficulty corresponding number:""")

    # Receive difficulty level selection from the client
    client_input = conn.recv(1024)
    difficulty_level = int(client_input.decode().strip())
    if difficulty_level == 1:
        guessme = generate_random_int(1, 50)
        leaderboard_filename = os.path.join(leaderboard_directory, "leaderboard_beginner.txt")
    elif difficulty_level == 2:
        guessme = generate_random_int(1, 100)
        leaderboard_filename = os.path.join(leaderboard_directory, "leaderboard_intermediate.txt")
    elif difficulty_level == 3:
        guessme = generate_random_int(1, 500)
        leaderboard_filename = os.path.join(leaderboard_directory, "leaderboard_challenger.txt")
    else:
        conn.sendall(b"Invalid difficulty level. Please enter a valid number (1-3): ")
        conn.close()
        continue

    # Send the game start banner
    conn.sendall(b"Let's start the game!\nEnter your guess:")

    tries = 0
    while True:
        # Receive user's guess
        client_input = conn.recv(1024)
        guess = int(client_input.decode().strip())
        tries += 1
        print(f"User guess attempt: {guess}")
        if guess == guessme:
            conn.sendall(b"Correct Answer!")  # Notify the client of correct guess
            break
        elif guess > guessme:
            conn.sendall(b"Guess Lower!\nEnter guess: ")  # Prompt user to guess lower
        elif guess < guessme:
            conn.sendall(b"Guess Higher!\nEnter guess:")  # Prompt user to guess higher

    # Update the leaderboard with user's name and score
    leaderboard[name] = tries

    # Save user's data into a file
    with open(leaderboard_filename, "a") as leaderboard_file:
        leaderboard_file.write(f"{name}: {tries} tries\n")

    # Close the connection
    conn.close()

# Display the leaderboard after all clients disconnect
print("\n=== Leaderboard ===")
for filename in os.listdir(leaderboard_directory):
    with open(os.path.join(leaderboard_directory, filename), "r") as leaderboard_file:
        print(f"\nLeaderboard for {filename}:")
        print(leaderboard_file.read())

# Close the server socket
s.close()
