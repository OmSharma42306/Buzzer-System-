import os
import socket
import threading
import time
from pygame import mixer
import pyttsx3

HOST = '127.0.0.1'
PORT = 5555

buzzer_lock = threading.Lock()
buzzed_groups = []
reset_event = threading.Event()  # Event to signal when it's okay to reset buzzers

mixer.init()
mixer.music.load('buzzer_sound.wav')

def handle_client(conn, addr, group):
    global buzzed_groups

    with buzzer_lock:
        if not reset_event.is_set():  # Check if it's okay to buzz
            print(f"Group {group} tried to buzz, but buzzers are locked.")
            conn.close()
            return

        buzzed_groups.append(group)
        print(f"Group {group} buzzed!")

        if len(buzzed_groups) == 1:
            print("Buzzer sound played!")
            mixer.music.play()

            # Use TTS to announce the buzzing group
            tts_engine = pyttsx3.init()
            tts_engine.say(f"Group {group} buzzed!")
            tts_engine.runAndWait()

    conn.close()

def reset_buzzer():
    global buzzed_groups
    with buzzer_lock:
        buzzed_groups = []
        reset_event.set()  # Set the event to allow buzzing again
        print("Waiting for buzzers...")

    # Schedule the reset_buzzer function to run again after 5 seconds
    threading.Timer(5, reset_buzzer).start()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Server listening on {HOST}:{PORT}")

    # Start the reset buzzer function
    reset_buzzer()

    while True:
        conn, addr = server.accept()

        # Wait for the event before allowing the client to buzz
        reset_event.wait()

        group = conn.recv(1024).decode()
        client_handler = threading.Thread(target=handle_client, args=(conn, addr, group))
        client_handler.start()

# Command-line server
print("Buzzer System Server")
print("Type 'exit' and press Enter to stop the server.")

server_thread = threading.Thread(target=start_server)
server_thread.start()

while True:
    user_input = input("> ")

    if user_input.lower() == 'exit':
        break
    else:
        print("Invalid command. Type 'exit' to stop the server.")
