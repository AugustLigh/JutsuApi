# JutsuApi 📺

**JutsuApi** — это простое Python API для работы с сайтом [JutSu](https://jut.su), предоставляющее удобные возможности для загрузки видео. Поддерживает три режима работы:  
- **Однопоточная загрузка**  
- **Синхронная загрузка**  
- **Асинхронная загрузка**

---

## 📦 Установка

Убедитесь, что у вас установлен Python 3.7 или выше. Затем установите зависимости:

```bash
pip install -r requirements.txt
```

🔧 Использование
Пример однопоточной загрузки видео:
```python
from JutSuApi import JutsuScraper
from JutSuApi import SingleThreadDownloader


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

```

# 🛠️ Требования
Python 3.10+
Библиотеки из requirements.txt

# 🤝 Содействие
Буду рад вашим вопросам, предложениям или баг-репортам! Оставляйте их в разделе Issues.

# 📜 Лицензия
Проект распространяется под лицензией MIT. Подробнее см. в LICENSE.
