import pyaudio
import numpy as np
from matplotlib import pyplot as plt

from src.util import (
    apply_window,
    band_pass,
    detect_frequency,
    freq_to_midi,
    smooth_signal,
)

# Set up audio stream
# reduce chunk size and sampling rate for lower latency
CHUNK_SIZE = 1024  # Number of audio frames per buffer
FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1  # Mono audio
RATE = 1024 * 8  # Audio sampling rate (Hz)
p = pyaudio.PyAudio()

# print info about audio devices
# let user select audio device
info = p.get_host_api_info_by_index(0)
numdevices = info.get("deviceCount")

for i in range(0, numdevices):
    if (p.get_device_info_by_host_api_device_index(0, i).get("maxInputChannels")) > 0:
        print(
            "Input Device id ",
            i,
            " - ",
            p.get_device_info_by_host_api_device_index(0, i).get("name"),
        )

print("select audio device:")
input_device = int(input())

# open audio input stream
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK_SIZE,
    input_device_index=input_device,
)

# set up interactive plot
fig = plt.figure()
ax = plt.gca()
(line,) = ax.plot(np.zeros(CHUNK_SIZE))
ax.set_ylim(-30000, 30000)

plt.ion()
plt.show()

# continuously capture and plot audio singal
while True:
    # Read audio data from stream
    data = stream.read(CHUNK_SIZE)

    # Convert audio data to numpy array
    data = np.frombuffer(data, dtype=np.int16)

    # Improve signal
    data = band_pass(data, lowcut=80, highcut=1000, fs=RATE)
    data = smooth_signal(data, window_size=64)
    data = apply_window(data, window_type="hamming")

    freq = detect_frequency(data, sample_rate=RATE)
    midi_note = freq_to_midi(freq)
    print(f"Frequency: {freq:.2f} Hz, MIDI Note: {midi_note}")
    line.set_ydata(data)

    # Redraw plot
    fig.canvas.draw()
    fig.canvas.flush_events()
