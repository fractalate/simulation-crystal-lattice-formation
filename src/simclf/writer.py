import json
import sys
import time
from datetime import datetime, timezone
from io import TextIOWrapper
from pathlib import Path
from typing import Dict

from simclf.typing import Point3DArray, check_point_3d_array

WRITER_OUTPUT_FILE_NAME_DEFAULT = "output.log"


class Writer():
    def __init__(
        self,
        simulation_name: str,
        simulation_version: str,
        output_directory: None | str | Path = None,
        output_file_name: None | str | Path = None,
        is_debug_enabled: None | bool = None,
    ):

        self.simulation_name: str = simulation_name
        self.simulation_version: str = simulation_version

        if output_directory is None:
            simulation_stamp: str = time.strftime("%Y%m%d-%H%M%S")
            self.output_directory: Path = (
                Path("out") / Path(f"{simulation_stamp}_{self.simulation_name}_{self.simulation_version}")
            )
        else:
            self.output_directory: Path = Path(output_directory)

        if output_file_name is None:
            self.output_file_name: Path = Path(WRITER_OUTPUT_FILE_NAME_DEFAULT)
        else:
            self.output_file_name: Path = Path(output_file_name)

        if is_debug_enabled is None:
            self.is_debug_enabled = False
        else:
            self.is_debug_enabled = is_debug_enabled

        self.text_streams: Dict[Path, TextIOWrapper] = {}
        self.timezone: None | timezone = None

    def ensure_output_directory_exists(self):
        output_directory = self.output_directory
        if not output_directory.is_dir():
            output_directory.mkdir(parents=True)
        return output_directory

    def write_points_to_csv(self, file_name: str | Path, points: Point3DArray, overwrite: bool = False):
        check_point_3d_array(points)

        file_path = self.ensure_output_directory_exists() / Path(file_name)

        if not overwrite:
            if file_path.exists():
                raise FileExistsError(file_path)  # XXX is this valid?

        with open(file_path, "w") as fout:
            for x, y, z in points:
                fout.write(f"{x},{y},{z}\n")

    def write_object_to_json(self, file_name: str | Path, obj: dict, overwrite: bool = False):
        file_path = self.ensure_output_directory_exists() / Path(file_name)

        if not overwrite:
            if file_path.exists():
                raise FileExistsError(file_path)  # XXX is this valid?

        with open(file_path, "w") as fout:
            fout.write(json.dumps(obj, indent=2))
            fout.write("\n")

    def write_document(self, file_name: str | Path, text: str, overwrite: bool = False):
        file_path = self.ensure_output_directory_exists() / Path(file_name)

        if not overwrite:
            if file_path.exists():
                raise FileExistsError(file_path)  # XXX is this valid?

        with open(file_path, "w") as fout:
            if text:
                fout.write(text)
                if text[-1] not in "\r\n":
                    fout.write("\n")

    def _get_text_stream(self, file_name: str | Path) -> TextIOWrapper:
        file_path = self.ensure_output_directory_exists() / Path(file_name)

        text_stream = self.text_streams.get(file_path)

        if text_stream is not None:
            return text_stream

        text_stream = open(file_path, "at")
        self.text_streams[file_path] = text_stream

        return text_stream

    def write_to_text_stream(self, file_name: str | Path, text: str):
        stream = self._get_text_stream(file_name)

        stream.write(text)
        stream.flush()

    def _write_to_text_stream_and_stdout(self, file_name: str | Path, text: str):
        self.write_to_text_stream(file_name, text)
        sys.stdout.write(text)

    def _now(self) -> datetime:
        if self.timezone is None:
            return datetime.now().astimezone()
        return datetime.now(tz=self.timezone)

    def _format_log_message(self, level: str, message: str):
        timestamp = self._now().strftime("%Y-%m-%dT%H:%M:%S.%f%z")
        return f"{timestamp} - {level} - {message}\n"

    def debug(self, message):
        if self.is_debug_enabled:
            self._write_to_text_stream_and_stdout(
                self.output_file_name,
                self._format_log_message("DEBUG", message),
            )

    def info(self, message):
        self._write_to_text_stream_and_stdout(
            self.output_file_name,
            self._format_log_message("INFO", message),
        )

    def warn(self, message):
        self._write_to_text_stream_and_stdout(
            self.output_file_name,
            self._format_log_message("WARN", message),
        )

    def error(self, message):
        self._write_to_text_stream_and_stdout(
            self.output_file_name,
            self._format_log_message("ERROR", message),
        )
