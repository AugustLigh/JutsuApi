import re

from .dto import VideoDataDTO

class VideoInfoParser:
    @staticmethod
    def parse(input_string: str) -> VideoDataDTO:
        pattern = re.compile(r'(\w+)\s*=\s*"(.*?)"|(\w+)\s*=\s*(\d+)|(\w+)\s*=\s*(yes|no)')
        matches = pattern.findall(input_string)
        
        data = {}
        for match in matches:
            key = match[0] or match[2] or match[4]
            value = match[1] or match[3] or match[5]
            if value.isdigit():
                value = int(value)
            elif value in {"yes", "no"}:
                value = value == "yes"
            data[key] = value

        return VideoDataDTO(
            anime=data.get("pview_anime", ""),
            category=data.get("pview_category", 0),
            type=data.get("pview_type", 0),
            season=data.get("pview_season", 0),
            episode=data.get("pview_episode", 0),
            intro_start=data.get("video_intro_start", 0),
            intro_end=data.get("video_intro_end", 0),
            music_intro=data.get("video_music_intro", ""),
            outro_start=data.get("video_outro_start", 0),
            music_outro=data.get("video_music_outro", ""),
            video_duration=data.get("this_video_duration", 0),
            new_player=data.get("jutsu_new_player", False)
        )