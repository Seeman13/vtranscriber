from abc import ABC, abstractmethod


class DataSaver(ABC):
    @abstractmethod
    def save(self, channel_id: str, content: str, destination: str):
        """
        Abstract method для сохранения данных.
        :param channel_id: ID канала.
        :param content: Текст, который нужно сохранить.
        :param destination: Местоназначение (путь к файлу или строка подключения к БД).
        """
        pass
