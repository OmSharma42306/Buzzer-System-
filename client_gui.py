import socket
import tkinter as tk
from tkinter import messagebox

HOST = '127.0.0.1'  # Change this to the server's IP address or use the loopback address
PORT = 5555
GROUP_NUMBER = "Royal Challengers Banglore"  # Change this to the group number for this client

def buzz():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            s.sendall(str(GROUP_NUMBER).encode())
            messagebox.showinfo("Buzzer Client", "Buzzed!")
        except socket.error as e:
            messagebox.showerror("Error", f"Unable to connect to the server:\n{e}")

# GUI setup
root = tk.Tk()
root.title(f"Group {GROUP_NUMBER} Buzzer Client")

# Event handler for the "Buzz" button
def buzz_button_pressed():
    buzz()

# Event handler for the "Exit" button
def exit_button_pressed():
    root.destroy()

# Create and configure GUI components
label = tk.Label(root, text=f"Group {GROUP_NUMBER} Buzzer Client", pady=10)
label.pack()

buzz_button = tk.Button(root, text="Buzz", command=buzz_button_pressed)
buzz_button.pack()

exit_button = tk.Button(root, text="Exit", command=exit_button_pressed)
exit_button.pack()

root.mainloop()
