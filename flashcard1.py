import tkinter as tk
from tkinter import ttk
import time
import winsound
import json
import os

class FlashcardApp:
    def __init__(self, master):
        self.master = master
        master.withdraw()

        self.flashcards_file = "flashyyy.json"
        self.flashcards = self.load_flashcards_from_file(self.flashcards_file)

        if not self.flashcards:
            print("❌ Flashcards not loaded. Check 'flashyyy.json'.")
            master.destroy()
            return

        self.current_flashcard_index = -1
        self.interval_ms = 3_600_000  # 1 hour
        self.display_duration_ms = 60_000  # ⚡ Show flashcard for 1 minute (60 sec)

        self.flashcard_window = None

        self.schedule_next_flashcard()

    def load_flashcards_from_file(self, filename):
        if not os.path.exists(filename):
            print(f"❌ File '{filename}' not found.")
            return []
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error loading JSON: {e}")
            return []

    def play_sound(self):
        try:
            winsound.Beep(800, 300)
        except:
            pass

    def show_flashcard(self):
        if self.flashcard_window:
            self.flashcard_window.destroy()

        self.play_sound()

        self.current_flashcard_index = (self.current_flashcard_index + 1) % len(self.flashcards)
        flashcard = self.flashcards[self.current_flashcard_index]

        self.flashcard_window = tk.Toplevel(self.master)
        self.flashcard_window.attributes('-fullscreen', True)
        self.flashcard_window.title("Flashcard")

        frame = ttk.Frame(self.flashcard_window, padding=50)
        frame.pack(expand=True)

        ttk.Label(frame, text=flashcard["title"], font=("Helvetica", 36, "bold")).pack(pady=30)
        ttk.Label(frame, text=flashcard["content"], font=("Helvetica", 24), wraplength=1400, justify="center").pack(pady=20)

        # 💣 Automatically close after 60 seconds
        self.flashcard_window.after(self.display_duration_ms, self.flashcard_window.destroy)

        # Schedule next flashcard after full interval
        self.master.after(self.interval_ms, self.show_flashcard)

    def schedule_next_flashcard(self):
        # Trigger the first flashcard immediately after 1 sec
        self.master.after(1000, self.show_flashcard)

if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()
