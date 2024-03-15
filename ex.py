# Import the necessary modules.
import tkinter
import pyaudio
import wave


class RecAUD:

    def __init__(
        self,
        chunk=1024,
        audio_format=pyaudio.paInt16,
        channels=2,
        rate_hz=44100,
    ):
        # Audio Properties
        self.CHUNK = chunk
        self.FORMAT = audio_format
        self.CHANNELS = channels
        self.RATE_HZ = rate_hz
        self.audio = pyaudio.PyAudio()
        self.frames = []
        self.is_recording = False

        # Start Tkinter and set Title
        self.main = tkinter.Tk()
        self.collections = []
        self.main.geometry("500x300")
        self.main.title("Record")

        # Set Input Select
        self.input_device = tkinter.StringVar(self.main)
        self.input_device.set(self.input_devices[0])
        self.input_device_select = tkinter.OptionMenu(
            self.main, self.input_device, *self.input_devices
        )
        self.input_device_select.pack()

        # Set Frames
        self.buttons = tkinter.Frame(self.main, padx=120, pady=20)

        # Pack Frame
        self.buttons.pack(fill=tkinter.BOTH)

        # Start and Stop buttons
        self.strt_rec = tkinter.Button(
            self.buttons,
            width=10,
            padx=10,
            pady=5,
            text="Start Recording",
            command=lambda: self.start_recording(),
        )
        self.strt_rec.grid(row=0, column=0, padx=50, pady=5)
        self.stop_rec = tkinter.Button(
            self.buttons,
            width=10,
            padx=10,
            pady=5,
            text="Stop Recording",
            command=lambda: self.stop_recording(),
        )
        self.stop_rec.grid(row=1, column=0, columnspan=1, padx=50, pady=5)

        tkinter.mainloop()

    @property
    def input_devices(self):
        output = []
        host_info = self.audio.get_host_api_info_by_index(0)
        for index in range(0, host_info.get("deviceCount")):
            device_info = self.audio.get_device_info_by_host_api_device_index(0, index)
            if (device_info.get("maxInputChannels")) > 0:
                device_name = device_info.get("name")
                output.append(f" {index} - {device_name}")
        return output

    def toggle_recording(self):
        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording()

    def start_recording(self):
        self.is_recording = True
        self.frames = []
        stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE_HZ,
            input=True,
            frames_per_buffer=self.CHUNK,
        )
        while self.is_recording:
            data = stream.read(self.CHUNK)
            self.frames.append(data)
            self.main.update()

        stream.close()

        wf = wave.open("test_recording.wav", "wb")
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE_HZ)
        wf.writeframes(b"".join(self.frames))
        wf.close()

    def stop_recording(self):
        self.is_recording = False


# Create an object of the ProgramGUI class to begin the program.
guiAUD = RecAUD()
