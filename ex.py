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
        self.record_button_text = tkinter.StringVar()
        self.record_button_text.set("Start Recording")
        self.record_button = tkinter.Button(
            self.buttons,
            width=10,
            padx=10,
            pady=5,
            textvariable=self.record_button_text,
            command=lambda: self.toggle_recording(),
        )
        self.record_button.grid(row=0, column=0, padx=50, pady=5)

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
        self.record_button_text.set("Stop Recording")
        self.is_recording = True
        self.frames = []
        self.record()
        self.save_recording()

    def stop_recording(self):
        self.record_button_text.set("Start Recording")
        self.is_recording = False

    def record(self):
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

    def save_recording(self):
        wave_file = wave.open("test_recording.wav", "wb")
        wave_file.setnchannels(self.CHANNELS)
        wave_file.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        wave_file.setframerate(self.RATE_HZ)
        wave_file.writeframes(b"".join(self.frames))
        wave_file.close()


# Create an object of the ProgramGUI class to begin the program.
guiAUD = RecAUD()
