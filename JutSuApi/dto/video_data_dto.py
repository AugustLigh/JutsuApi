from dataclasses import dataclass

__all__ = ("VideoDataDTO")

@dataclass
class VideoDataDTO:
    anime: str
    category: int
    type: int
    season: int
    episode: int
    intro_start: int
    intro_end: int
    music_intro: str
    outro_start: int
    music_outro: str
    video_duration: int
    new_player: bool