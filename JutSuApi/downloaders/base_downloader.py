import os
from abc import ABC, abstractmethod

class BaseDownloader(ABC):
    """Базовый класс для загрузчиков."""

    def __init__(self, url: str, output_folder: str, **kwargs):
        self.url = url
        self.output_folder = output_folder
        self.local_filename = os.path.basename(self.url.split("?")[0])
        self.output_file = os.path.join(self.output_folder, self.local_filename)
        os.makedirs(self.output_folder, exist_ok=True)

    @abstractmethod
    def download(self) -> str:
        """Метод для загрузки файла."""
        pass