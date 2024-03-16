import hashlib
import tkinter
import pyaudio
import pydub


class AudioRecorder:
    def __init__(self):
        # Audio Properties
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE_HZ = 44100
        self.audio = pyaudio.PyAudio()
        self.frames = []
        self.is_recording = False

        # Script
        self.script_lines = [
            "This is an example script line.",
            "I should also read this second line.",
            "This is the final line.",
        ]
        self.script_current_index = 0

        # Start Tkinter and set Title
        self.main = tkinter.Tk()
        self.main.geometry("500x300")
        self.main.title("Record")

        # Load Script Button
        self.load_script_button = tkinter.Button(
            self.main,
            width=10,
            padx=10,
            pady=5,
            text="Load Script",
            command=lambda: self.load_script(),
        )
        self.record_button.pack()

        # Set Input Select
        self.input_device = tkinter.StringVar(self.main)
        self.input_device.set(self.input_devices[0])
        self.input_device_select = tkinter.OptionMenu(
            self.main, self.input_device, *self.input_devices
        )
        self.input_device_select.pack()

        # Record Button
        self.record_button_text = tkinter.StringVar()
        self.record_button_text.set("Start Recording")
        self.record_button = tkinter.Button(
            self.main,
            width=10,
            padx=10,
            pady=5,
            textvariable=self.record_button_text,
            command=lambda: self.toggle_recording(),
        )
        self.record_button.pack()

        # Next Button
        self.next_button = tkinter.Button(
            self.main,
            width=10,
            padx=10,
            pady=5,
            text="Next",
            command=lambda: self.load_next_line(),
        )
        self.next_button.pack()

        # Previous Button
        self.previous_button = tkinter.Button(
            self.main,
            width=10,
            padx=10,
            pady=5,
            text="Prev",
            command=lambda: self.load_prev_line(),
        )
        self.previous_button.pack()

        self.current_line = tkinter.StringVar()
        self.load_line()
        self.current_line_label = tkinter.Label(
            self.main,
            textvariable=self.current_line,
            padx=10,
            pady=5,
        )
        self.current_line_label.pack()

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

    ###################
    # Script Controls #
    ###################

    @property
    def current_line_hash(self):
        return hashlib.md5(
            self.script_lines[self.script_current_index].encode("utf-8")
        ).hexdigest()[0:16]

    def load_next_line(self):
        if self.is_recording:
            return
        self.script_current_index = (self.script_current_index + 1) % len(
            self.script_lines
        )
        self.load_line()

    def load_prev_line(self):
        if self.is_recording:
            return
        self.script_current_index = (self.script_current_index - 1) % len(
            self.script_lines
        )
        self.load_line()

    def load_line(self):
        self.current_line.set(self.script_lines[self.script_current_index])

    def load_script(self):
        pass

    ######################
    # Recording Controls #
    ######################

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
        audio_segment = pydub.AudioSegment(
            b"".join(self.frames),
            sample_width=self.audio.get_sample_size(self.FORMAT),
            channels=self.CHANNELS,
            frame_rate=self.RATE_HZ,
        )
        # High Pass Filter
        HIGH_PASS_FILTER_CUTOFF_HZ = 80
        audio_segment.high_pass_filter(HIGH_PASS_FILTER_CUTOFF_HZ)
        # Normalize
        NORMALIZE_HEADROOM = 0.1
        audio_segment.normalize(NORMALIZE_HEADROOM)
        # Trim silence
        # TODO: Make better maybe
        MIN_SILENCE_LENGTH_MS = 1000
        SILENCE_THRESHOLD = -16
        PADDING_MS = 100
        audio_segment.strip_silence(
            silence_len=MIN_SILENCE_LENGTH_MS,
            silence_thresh=SILENCE_THRESHOLD,
            padding=PADDING_MS,
        )
        audio_segment.export(out_f=f"{self.current_line_hash}.wav", format="wav")


if __name__ == "__main__":
    AudioRecorder = AudioRecorder()
