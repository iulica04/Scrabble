import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

from DictionaryProcessor import DictionaryProcessor
from Game import Game
import os

class MainGUI:
    """
    Represents the main GUI for the Scrabble game.

    Attributes:
        root (tk.Tk): The root window of the GUI.
        background_image (tk.PhotoImage): The background image for the GUI.
        background_label (tk.Label): The label to display the background image.
        upload_button (ttk.Button): The button to upload the dictionary file.
        start_button (ttk.Button): The button to start the game.
        dictionary_path (str): The path to the uploaded dictionary file.
    """

    def __init__(self, root):
        """
        Initializes the MainGUI with the given root window.

        Args:
            root (tk.Tk): The root window of the GUI.
        """
        self.root = root
        self.root.title("Scrabble Game")
        self.root.geometry("800x600")

        self.background_image = tk.PhotoImage(file="D:\\Scrubble\\Utils\\Scrabble.png")
        self.background_label = tk.Label(root, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton", background="#a6a6a6", foreground="black", borderwidth=3,
                        focuscolor='#6b597f', font=('Helvetica', 12))
        style.map("TButton", background=[('active', '#5c6b8b')])

        style.configure("Start.TButton", background="#a6a6a6", foreground="black", borderwidth=3,
                        focuscolor='#6b597f', font=('Helvetica', 12))
        style.map("Start.TButton", background=[('active', '#5c6b8b')])

        self.upload_button = ttk.Button(root, text="Upload Dictionary", command=self.upload_file, style="TButton")
        self.upload_button.pack(pady=(400, 20), padx=20, ipadx=20, ipady=10)

        self.start_button = ttk.Button(root, text="Start Game", command=self.start_game, style="Start.TButton")
        self.start_button.pack(pady=10, padx=20, ipadx=20, ipady=10)

        self.dictionary_path = None

    def upload_file(self):
        """
        Opens a file dialog to upload a dictionary file.
        """
        self.dictionary_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if self.dictionary_path:
            file_name = os.path.basename(self.dictionary_path)
            self.upload_button.config(text=file_name)
            self.start_button.config(state=tk.NORMAL)

    def start_game(self):
        """
        Starts the Scrabble game if a dictionary file is uploaded.
        """
        if self.dictionary_path:
            processor = DictionaryProcessor(self.dictionary_path)
            processor.load_dictionary()
            game = Game(dictionary_path=self.dictionary_path)
            self.root.destroy()  # Close the main window
            game.run()
        else:
            messagebox.showerror("Error", "Please upload a dictionary file first")

if __name__ == "__main__":
    root = tk.Tk()
    gui = MainGUI(root)
    root.mainloop()