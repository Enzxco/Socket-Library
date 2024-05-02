import socket
import random

host = "0.0.0.0"
port = 7777
banner = """
== Guessing Game v1.0 ==
Difficulty Level
1. Beginner (1-50)
2. Intermediate (1-100)
3. Challenger (1-500)
Enter the difficulty corresponding number:"""

def generate_random_int(low, high):
    return random.randint(low, high)

# initialize the socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

print(f"Server is listening on port {port}")
guessme = 0
conn = None
while True:
    if conn is None:
        print("Waiting for connection..")
        conn, addr = s.accept()
        print(f"New client: {addr[0]}")
        # Send the difficulty selection banner
        conn.sendall(banner.encode())
    else:
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
            continue
        
        # Send the game start banner
        conn.sendall(b"Let's start the game!\nEnter your guess:")

        while True:
            client_input = conn.recv(1024)
            guess = int(client_input.decode().strip())
            print(f"User guess attempt: {guess}")
            if guess == guessme:
                conn.sendall(b"Correct Answer!")
                conn.close()
                conn = None
                break
            elif guess > guessme:
                conn.sendall(b"Guess Lower!\nEnter guess: ")
                continue
            elif guess < guessme:
                conn.sendall(b"Guess Higher!\nEnter guess:")
                continue
