import tkinter as tk

from analyse import analyse
from record import record


def calm_down(cd, i=10):
    if i > 0:
        cd.config(text=f"{i}")
        cd.after(1000, calm_down, cd, i - 1)
    else:
        cd.config(text="")


class Emmy:
    def __init__(self, window):
        self.window = window
        self.outfile = "recording.wav"
        self.emotion = None
        self.colour = None

        self.label = tk.Label(self.window, text="")
        self.label.pack()  # Must be separate to avoid None

        self.countdown = tk.Label(self.window, text="")
        self.countdown.pack()

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
                self.colour = "black"

            case ["hap"]:
                self.emotion = "happy"
                self.colour = "yellow"

            case ["ang"]:
                self.emotion = "angry"
                self.colour = "red"

            case ["sad"]:
                self.emotion = "sad"
                self.colour = "blue"

        self.update_emotion()

        if self.emotion_dict == ["ang"]:
            calm_down(self.countdown)

    def update_emotion(self):
        self.label.config(
            text=f"Detected emotion: {self.emotion}", fg=self.colour
        )

    def get_emotion(self):
        return self.emotion


window = tk.Tk()
window.geometry("200x90")
emmy = Emmy(window)

window.mainloop()
