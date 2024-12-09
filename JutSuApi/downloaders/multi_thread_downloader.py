import os

from tqdm import tqdm
from ..constants import SessionSingleton
from .base_downloader import BaseDownloader
from concurrent.futures import ThreadPoolExecutor

# __all__ = ("MultiThreadDownloader",)

class MultiThreadDownloader(BaseDownloader):
    def __init__(self, url: str, output_folder: str, threads: int = 4):
        super().__init__(url, output_folder)
        self.threads = threads
        self.temp_folder = os.path.join(self.output_folder, "temp")
        os.makedirs(self.temp_folder, exist_ok=True)

    def get_file_size(self) -> int:
        response = SessionSingleton.get_instance().head(self.url)
        response.raise_for_status()
        return int(response.headers.get("Content-Length", 0))

    def download_segment(self, start: int, end: int, part_num: int):
        headers = {"Range": f"bytes={start}-{end}"}
        temp_file = os.path.join(self.temp_folder, f"part_{part_num}")

        with SessionSingleton.get_instance().get(self.url, headers=headers, stream=True) as response:
            response.raise_for_status()
            with open(temp_file, "wb") as file:
                for chunk in response.iter_content(chunk_size=512 * 1024):
                    file.write(chunk)

    def merge_segments(self):
        with open(self.output_file, "wb") as output:
            for part_num in range(self.threads):
                temp_file = os.path.join(self.temp_folder, f"part_{part_num}")
                with open(temp_file, "rb") as part:
                    output.write(part.read())
                os.remove(temp_file)

    def download(self) -> str:
        file_size = self.get_file_size()
        part_size = file_size // self.threads
        ranges = [
            (i * part_size, (i + 1) * part_size - 1 if i < self.threads - 1 else file_size - 1)
            for i in range(self.threads)
        ]

        print(f"Starting download with {self.threads} threads...")
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            list(
                tqdm(
                    executor.map(
                        lambda args: self.download_segment(*args),
                        [(start, end, idx) for idx, (start, end) in enumerate(ranges)]
                    ),
                    total=self.threads,
                    desc="Downloading",
                )
            )

        self.merge_segments()
        print(f"Download completed: {self.output_file}")
        return self.output_file