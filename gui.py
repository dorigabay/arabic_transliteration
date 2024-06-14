import os.path
import tkinter as tk
from tkinter import filedialog
import os
import webbrowser
from logic import arabic_to_hebrew


class Transliterator:
    def __init__(self, root):
        self.root = root
        self.root.title("Arabic to Hebrew Transliteration")

        self.github_link = tk.Label(root, text="© Dor Gabay 2024 | GitHub Repository", fg="blue", cursor="hand2")
        self.github_link.grid(row=4, column=0, columnspan=2)
        self.github_link.bind("<Button-1>", self.open_github_link)

        self.arabic_entry = tk.Entry(root, width=50)
        self.arabic_entry.grid(row=0, column=0, padx=10, pady=10)

        self.transliteration_button = tk.Button(root, text="Transliterate", command=self.transliterate)
        self.transliteration_button.grid(row=0, column=1, padx=10, pady=10)

        self.transliteration_label = tk.Label(root, text="", wraplength=400)
        self.transliteration_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.save_button = tk.Button(root, text="Save", command=self.save_to_file)
        self.save_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.status_label = tk.Label(root, text="", fg="red")
        self.status_label.grid(row=3, column=0, columnspan=2)

    def open_github_link(self, event):
        webbrowser.open_new("https://github.com/dorigabay/arabic_transliteration")

    def transliterate(self):
        arabic_text = self.arabic_entry.get()
        transliteration, original_text = arabic_to_hebrew(arabic_text)
        self.transliteration_label.config(text=transliteration)
        self.status_label.config(text="Happy with the result?\nPlease let us know how to improve via GitHub.", fg="black")

    def save_to_file(self):
        arabic_text = self.arabic_entry.get()
        transliteration, original_text = arabic_to_hebrew(arabic_text)
        output_path = tk.filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        with open(os.path.join(output_path), "w", encoding="utf-8") as file:
            file.write(arabic_text + '\n')
            file.write(transliteration)
        self.status_label.config(text="Transcription saved to transliteration.txt", fg="green")


def create_gui():
    root = tk.Tk()
    app = Transliterator(root)
    root.mainloop()


