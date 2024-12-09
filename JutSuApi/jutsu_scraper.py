import re
import base64
from bs4 import BeautifulSoup

from .dto.video_info_dto import VideoInfoDTO
from .video_info_parser import VideoInfoParser
from .constants import SessionSingleton

__all__ = ("JutsuScraper",)

class JutsuScraper:
    """Класс для работы с сайтом Jutsu."""
    def __init__(self, url: str):
        self.url = url
        self.soup = None
        self.base64_data = None
        self.video_data = {}
        self.fetch_page()

    def fetch_page(self):
        response = SessionSingleton.get_instance().get(self.url)
        response.raise_for_status()
        self.soup = BeautifulSoup(response.text, 'html.parser')
        self.base64_data = self._extract_base64_data(response.text)

    def _extract_base64_data(self, page_content: str) -> str:
        base64_match = re.search("Base64.decode\\( \"(.*)\" \\)", page_content)
        if not base64_match:
            raise ValueError("Base64 data not found")
        return base64.b64decode(base64_match.group(1)).decode("utf-8")

    def get_video_info(self) -> VideoInfoDTO:
        if not self.base64_data:
            raise ValueError("Base64 data not fetched or decoded")
        video_data = VideoInfoParser.parse(self.base64_data)

        meta_tag = self.soup.find("meta", property="og:image")
        poster = meta_tag["content"] if meta_tag else ""
        name = self.soup.find("h2").text

        return VideoInfoDTO(
            video_data=video_data,
            poster=poster,
            episode_name=name
        )

    def get_video_sources(self):
        if not self.soup:
            raise ValueError("Page content not fetched")
        sources = self.soup.find_all("source")
        for source in sources:
            quality = source.get("res")
            video_url = source.get("src")
            if quality and video_url:
                self.video_data[quality] = video_url
        return self.video_data