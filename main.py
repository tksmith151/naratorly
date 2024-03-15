import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pyaudio
import wave

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 512
RECORD_SECONDS = 1
WAVE_OUTPUT_FILENAME = "recordedFile.wav"
device_index = 2
audio = pyaudio.PyAudio()

info = audio.get_host_api_info_by_index(0)
numdevices = info.get("deviceCount")
audio_device_strings = []
for i in range(0, numdevices):
    if (
        audio.get_device_info_by_host_api_device_index(0, i).get("maxInputChannels")
    ) > 0:
        audio_device_name = audio.get_device_info_by_host_api_device_index(0, i).get(
            "name"
        )
        audio_device_strings.append(f" {i} - {audio_device_name}")

window = tk.Tk()
window.title("Combobox")
window.geometry("500x250")

# label text for title
"""
ttk.Label(
    window,
    text="GFG Combobox Widget",
    background="green",
    foreground="white",
    font=("Times New Roman", 15),
).grid(row=0, column=1)
"""

# label
ttk.Label(window, text="Audio Input:", font=("Times New Roman", 10)).grid(
    column=0, row=5, padx=10, pady=25
)

# Combobox creation
n = tk.StringVar()
audio_input_select = ttk.Combobox(window, width=27, textvariable=n)

# Adding combobox drop down list
audio_input_select["values"] = audio_device_strings

audio_input_select.grid(column=1, row=5)
audio_input_select.current(0)


def start_recording():
    input_device_index = int(audio_input_select.get().split(" ")[1])
    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        input_device_index=input_device_index,
        frames_per_buffer=CHUNK,
    )
    Recordframes = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        Recordframes.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, "wb")
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b"".join(Recordframes))
    waveFile.close()


def stop_recording():
    pass


def load_next_line():
    pass


def load_prev_line():
    pass


btn = ttk.Button(window, text="Start Recording", command=start_recording)
btn.place(relx="0.5", rely="0.5")

window.mainloop()

"""

index = int(input())
print("recording via index " + str(index))

stream = audio.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    input_device_index=index,
    frames_per_buffer=CHUNK,
)
print("recording started")
Recordframes = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    Recordframes.append(data)
print("recording stopped")

stream.stop_stream()
stream.close()
audio.terminate()

waveFile = wave.open(WAVE_OUTPUT_FILENAME, "wb")
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b"".join(Recordframes))
waveFile.close()

"""
