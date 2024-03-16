import pathlib
import tkinter
from tkinter import filedialog

from audio_processor import AudioProcessor
from file_system_connector import FileSystemConnector
from script_handler import ScriptHandler


class AudioRecorder:
    def __init__(self):
        # Modules
        self.audio = AudioProcessor()
        self.connector = FileSystemConnector()
        self.script = ScriptHandler()

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
            command=lambda: self.handle_load_script_button(),
        )
        self.load_script_button.pack()

        # Set Input Select
        self.input_device_value = tkinter.StringVar(self.main)
        self.input_device_value.set(self.audio.input_devices[0])
        self.input_device_select = tkinter.OptionMenu(
            self.main,
            self.input_device_value,
            *self.audio.input_devices,
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
            command=lambda: self.handle_record_button(),
        )
        self.record_button.pack()

        # Next Button
        self.next_button = tkinter.Button(
            self.main,
            width=10,
            padx=10,
            pady=5,
            text="Next",
            command=lambda: self.handle_next_button(),
        )
        self.next_button.pack()

        # Previous Button
        self.previous_button = tkinter.Button(
            self.main,
            width=10,
            padx=10,
            pady=5,
            text="Prev",
            command=lambda: self.handle_previous_button(),
        )
        self.previous_button.pack()

        # Previous Line
        self.previous_line_value = tkinter.StringVar()
        self.previous_line_label = tkinter.Label(
            self.main,
            textvariable=self.previous_line_value,
        )
        self.previous_line_label.pack()

        # Current Line
        self.current_line_value = tkinter.StringVar()
        self.current_line_label = tkinter.Label(
            self.main,
            textvariable=self.current_line_value,
        )
        self.current_line_label.pack()

        # Next Line
        self.next_line_value = tkinter.StringVar()
        self.mext_line_label = tkinter.Label(
            self.main,
            textvariable=self.next_line_value,
        )
        self.mext_line_label.pack()

        self.load_line()

    def run(self):
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

    ######################
    # Recording Controls #
    ######################

    def handle_load_script_button(self):
        self.load_script_file_path()

    def handle_record_button(self):
        if self.audio.is_recording:
            self.stop_recording()
        else:
            self.start_recording()

    def handle_next_button(self):
        self.script.load_next_line()
        self.load_line()

    def handle_previous_button(self):
        self.script.load_previous_line()
        self.load_line()

    ######################
    # State Transistions #
    ######################

    def start_recording(self):
        self.audio.start_recording()
        self.record()

    def stop_recording(self):
        self.audio.stop_recording()

    def load_line(self):
        self.previous_line_value.set(self.script.previous_line)
        self.current_line_value.set(self.script.current_line)
        self.next_line_value.set(self.script.next_line)

    def load_script_file_path(self):
        filename = filedialog.askopenfilename(
            filetypes=(
                ("txt file", "*.txt"),
                ("All files", "*.*"),
            )
        )
        if filename:
            self.connector.script_file_path = pathlib.Path(filename)
            self.load_script()

    def load_script(self):
        lines = self.connector.load_script_lines()
        self.script.load_script(lines)
        self.load_line()

    ###########
    # Helpers #
    ###########

    def record(self):
        self.record_button_text.set("Stop Recording")
        self.audio.open_stream()
        while self.audio.is_recording:
            self.main.update()
            self.audio.record_chunk()
        self.audio.close_stream()
        self.record_button_text.set("Start Recording")
        audio_segment = self.audio.process_recoding()
        self.connector.save_audio(audio_segment, self.script.current_line_hash)


if __name__ == "__main__":
    AudioRecorder = AudioRecorder()
