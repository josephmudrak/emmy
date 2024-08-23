import tkinter as tk

from analyse import analyse
from record import record

outfile = "recording.wav"

window = tk.Tk()
window.title("EMMY")


def record_button_handler():
    record(44100, 5, outfile=outfile)
    analyse(outfile=outfile)


record_button = tk.Button(
    text="Start Recording", command=record_button_handler
)
record_button.pack()

# Start event loop
window.mainloop()
