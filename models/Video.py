class Video:
    def __init__(self, url: str, title: str, subtitles: str):
        """
        Инициализирует объект Video с URL, названием и субтитрами.
        :param url: Ссылка на видео.
        :param title: Название видео.
        :param subtitles: Текст субтитров.
        """
        self.url = url
        self.title = title
        self.subtitles = subtitles
