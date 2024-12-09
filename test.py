from JutSuApi import JutsuScraper
from JutSuApi import SingleThreadDownloader


# Пример использования
def main():
    url = "https://jut.su/nier-automata/episode-7.html"
    output_folder = "videos"

    scraper = JutsuScraper(url)

    video_info = scraper.get_video_info()
    print(f"Video duration: {video_info.video_data.video_duration}")
    
    print(f"Poster: {video_info.poster}")

    video_sources = scraper.get_video_sources()
    print("Available qualities:", sorted(video_sources.keys(), reverse=True))

    selected_quality = input("Choose quality (e.g., 1080): ")
    if selected_quality not in video_sources:
        print("Selected quality not available.")
        return

    downloader = SingleThreadDownloader(video_sources[selected_quality], output_folder)
    downloader.download()

if __name__ == "__main__":
    main()
