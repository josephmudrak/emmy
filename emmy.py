import tkinter as tk

from analyse import analyse
from record import record


class Emmy:
    def __init__(self, window):
        self.window = window
        self.outfile = "recording.wav"
        self.emotion = None

        self.label = tk.Label(self.window, text="")
        self.label.pack()  # Must be separate to avoid None

        self.window.title("EMMY")

        self.record_button = tk.Button(
            self.window,
            text="Start Recording",
            command=self.record_button_handler,
        ).pack()

    def record_button_handler(self):
        self.label.config(text="Recording…")
        self.window.update_idletasks()
        record(44100, 5, outfile=self.outfile)

        self.label.config(text="Detecting emotion…")
        self.window.update_idletasks()
        self.emotion_dict = analyse(outfile=self.outfile)

        match self.emotion_dict:
            case ["neu"]:
                self.emotion = "neutral"

            case ["hap"]:
                self.emotion = "happy"

            case ["ang"]:
                self.emotion = "angry"

            case ["sad"]:
                self.emotion = "sad"

        self.update_emotion()

    def update_emotion(self):
        self.label.config(text=f"Detected emotion: {self.emotion}")

    def get_emotion(self):
        return self.emotion


window = tk.Tk()
window.geometry("200x60")
emmy = Emmy(window)

window.mainloop()
