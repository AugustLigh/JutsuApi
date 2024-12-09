import os

from tqdm import tqdm
from ..constants import SessionSingleton
from .base_downloader import BaseDownloader

class SingleThreadDownloader(BaseDownloader):
    def __init__(self, url: str, output_folder: str, chunk_size: int = 512 * 1024):
        super().__init__(url, output_folder)
        self.chunk_size = chunk_size

    def download(self) -> str:
        temp_file = self.output_file + ".temp"

        resume_size = os.stat(temp_file).st_size if os.path.exists(temp_file) else 0
        headers = {"Range": f"bytes={resume_size}-", "Accept-Encoding": "gzip, deflate, br",}

        with SessionSingleton.get_instance().get(self.url, headers=headers, stream=True) as response:
            response.raise_for_status()
            total_size = int(response.headers.get("Content-Length", 0)) + resume_size

            with tqdm(total=total_size, initial=resume_size, unit="B", unit_scale=True, desc="Downloading") as progress_bar:
                with open(temp_file, "ab") as temp_file_handle:
                    for chunk in response.iter_content(chunk_size=self.chunk_size):
                        temp_file_handle.write(chunk)
                        progress_bar.update(len(chunk))

        os.rename(temp_file, self.output_file)
        print(f"Download completed: {self.output_file}")
        return self.output_file