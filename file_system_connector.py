from pydub import AudioSegment
from pathlib import Path
import error
import os


class FileSystemConnector:
    def __init__(self) -> None:
        self.script_file_path: Path = None

    @property
    def is_ready(self):
        return self.script_file_path is not None

    @property
    def line_audio_directory(self):
        if self.is_ready:
            return self.script_file_path.parent / "line_audio"

    def load_script_lines(self):
        lines = []
        if self.is_ready:
            with open(self.script_file_path) as file_descriptor:
                lines = file_descriptor.readlines()
        return lines

    def save_audio(self, audio_segment: AudioSegment, line_hash: str):
        if not self.is_ready:
            raise error.NaratorlyError("Must select script file first")
        os.makedirs(self.line_audio_directory, exist_ok=True)
        file_path = self.line_audio_directory / f"{line_hash}.wav"
        audio_segment.export(out_f=str(file_path), format="wav")
