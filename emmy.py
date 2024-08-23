from analyse import analyse
from record import record

outfile = "recording.wav"

record(44100, 5, outfile)
analyse(outfile)
