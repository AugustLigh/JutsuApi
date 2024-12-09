import aiohttp

from tqdm import tqdm
from .base_downloader import BaseDownloader

__all__ = ("AsyncDownloader",)

class AsyncDownloader(BaseDownloader):
    def __init__(self, url: str, output_folder: str, chunk_size: int = 512 * 1024):
        super().__init__(url, output_folder)
        self.chunk_size = chunk_size

    async def get_file_size(self) -> int:
        async with aiohttp.ClientSession() as session:
            async with session.head(self.url, headers={"User-Agent": "Mozilla/5.0"}) as response:
                response.raise_for_status()
                return int(response.headers.get("Content-Length", 0))

    async def download(self) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, headers={"User-Agent": "Mozilla/5.0"}, timeout=60) as response:
                response.raise_for_status()
                total_size = int(response.headers.get("Content-Length", 0))

                with open(self.output_file, "wb") as file:
                    progress_bar = tqdm(
                        total=total_size,
                        unit="B",
                        unit_scale=True,
                        unit_divisor=1024,
                        desc="Downloading",
                    )
                    async for chunk in response.content.iter_chunked(self.chunk_size):
                        file.write(chunk)
                        progress_bar.update(len(chunk))
                    progress_bar.close()

        print(f"Download completed: {self.output_file}")
        return self.output_file