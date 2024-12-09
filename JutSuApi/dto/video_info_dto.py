from dataclasses import dataclass
from .video_data_dto import VideoDataDTO

__all__ = ("VideoInfoDTO",)

@dataclass
class VideoInfoDTO:
    video_data: VideoDataDTO
    poster: str
    episode_name: str