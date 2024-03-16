import pathlib
import pyaudio
import pydub

#############
# Constants #
#############


class AudioProcessor:
    def __init__(self) -> None:
        self.frames_per_buffer = 1024
        self.format = pyaudio.paInt16
        self.channels = 2
        self.rate = 44100  # HZ
        self.audio = pyaudio.PyAudio()
        self.frames = []
        self.is_recording = False
        self.stream = None
        self.audio_segment = None
        self.input_device_index = 0

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

    def set_input_device(self, input_device: str):
        self.input_device_index = int(input_device.split(" ")[1])

    def open_stream(self):
        self.stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.frames_per_buffer,
            input_device_index=self.input_device_index,
        )

    def close_stream(self):
        self.stream.close()

    def start_recording(self):
        self.is_recording = True
        self.reset_recording()
        self.open_stream()

    def reset_recording(self):
        self.frames = []

    def record_chunk(self):
        data = self.stream.read(self.frames_per_buffer)
        self.frames.append(data)

    def stop_recording(self):
        self.is_recording = False

    def save_recording(self, file_path: pathlib.Path):
        self.process_recoding()
        self.audio_segment.export(out_f=str(file_path), format="wav")

    def process_recoding(self):
        self.audio_segment = pydub.AudioSegment(
            b"".join(self.frames),
            sample_width=self.audio.get_sample_size(self.format),
            channels=self.channels,
            frame_rate=self.rate,
        )
        # High Pass Filter
        HIGH_PASS_FILTER_CUTOFF_HZ = 80
        self.audio_segment.high_pass_filter(HIGH_PASS_FILTER_CUTOFF_HZ)
        # Normalize
        NORMALIZE_HEADROOM = 0.1
        self.audio_segment.normalize(NORMALIZE_HEADROOM)
        # Trim silence
        # TODO: Make better maybe
        MIN_SILENCE_LENGTH_MS = 1000
        SILENCE_THRESHOLD = -16
        PADDING_MS = 100
        self.audio_segment.strip_silence(
            silence_len=MIN_SILENCE_LENGTH_MS,
            silence_thresh=SILENCE_THRESHOLD,
            padding=PADDING_MS,
        )
        return self.audio_segment
