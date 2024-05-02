import socket

host = "192.168.56.1"
port = 7777

def play_game():
    s = socket.socket()
    s.connect((host, port))

    # received the banner
    print(s.recv(1024).decode().strip())

    while True:
        user_input = input("").strip()
        s.sendall(user_input.encode())
        reply = s.recv(1024).decode().strip()
        if "Correct" in reply:
            print(reply)
            break
        print(reply)
        continue

    s.close()

# Main loop to play the game
while True:
    play_game()
    print("\nDo you want to:")
    print("(A) Play Again")
    print("(B) Quit")
    choice = input("Enter key: ")
    if choice != "A":
        print("Thank you for playing!")
        break
