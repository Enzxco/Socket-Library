import socket
import random

host = "0.0.0.0"
port = 7777
banner = """
== Guessing Game v1.0 ==
Enter your name:"""

def generate_random_int(low, high):
    return random.randint(low, high)

# Initialize the socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

print(f"Server is listening on port {port}")

# Define the leaderboard dictionary to store user scores
leaderboard = {}

while True:
    conn, addr = s.accept()
    print(f"New client connected: {addr[0]}")
    conn.sendall(banner.encode())

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

    client_input = conn.recv(1024)
    difficulty_level = int(client_input.decode().strip())
    if difficulty_level == 1:
        guessme = generate_random_int(1, 50)
    elif difficulty_level == 2:
        guessme = generate_random_int(1, 100)
    elif difficulty_level == 3:
        guessme = generate_random_int(1, 500)
    else:
        conn.sendall(b"Invalid difficulty level. Please enter a valid number (1-3): ")
        conn.close()
        continue

    # Send the game start banner
    conn.sendall(b"Let's start the game!\nEnter your guess:")

    tries = 0
    while True:
        client_input = conn.recv(1024)
        guess = int(client_input.decode().strip())
        tries += 1
        print(f"User guess attempt: {guess}")
        if guess == guessme:
            conn.sendall(b"Correct Answer!")
            break
        elif guess > guessme:
            conn.sendall(b"Guess Lower!\nEnter guess: ")
        elif guess < guessme:
            conn.sendall(b"Guess Higher!\nEnter guess:")

    # Update the leaderboard with user's name and score
    leaderboard[name] = tries

    conn.close()

# Display the leaderboard after all clients disconnect
print("\n=== Leaderboard ===")
for name, score in sorted(leaderboard.items(), key=lambda x: x[1]):
    print(f"{name}: {score} tries")

s.close()
