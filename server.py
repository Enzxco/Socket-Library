import socket
import random

host = "0.0.0.0"
port = 7777
banner = """

== Guessing Game v1.0 ==
Choose the difficulty level:
a. Beginner (1-50)
b. Intermediate (1-100)
c. Challenger (1-500)

Enter your guess:"""

def generate_random_int(low, high):
    return random.randint(low, high)

# initialize the socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

print(f"server is listening in port {port}")

while True:
    conn, addr = s.accept()
    print(f"new client: {addr[0]}")

    # Send difficulty options to the client
    conn.sendall(banner.encode())

    # Receive difficulty choice from the client
    try:
        difficulty_choice = conn.recv(1024).decode().strip()
    except ConnectionAbortedError:
        print("Client closed the connection unexpectedly")
        continue

    while True:
        guessme = generate_random_int(1, 100)  # Default range if no choice is made
        if difficulty_choice == 'a':
            guessme = generate_random_int(1, 50)
        elif difficulty_choice == 'b':
            guessme = generate_random_int(1, 100)
        elif difficulty_choice == 'c':
            guessme = generate_random_int(1, 500)

        cheat_str = f"==== number to guess is {guessme} \n" + banner
        conn.sendall(cheat_str.encode())

        while True:
            try:
                client_input = conn.recv(1024)
            except ConnectionAbortedError:
                print("Client closed the connection unexpectedly")
                break

            if not client_input:
                print("Client closed the connection")
                break

            guess = int(client_input.decode().strip())
            print(f"User guess attempt: {guess}")
            if guess == guessme:
                conn.sendall(b"Correct Answer!\nIf retry game, press Y if not press N\n")
                break
            elif guess > guessme:
                conn.sendall(b"Guess Lower!\nenter guess: ")
            elif guess < guessme:
                conn.sendall(b"Guess Higher!\nenter guess:")
