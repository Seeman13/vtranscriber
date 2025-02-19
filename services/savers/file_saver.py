import logging
import os
import json
from datetime import datetime

from .data_saver import DataSaver

logger = logging.getLogger('app_logger')

class FileSaver(DataSaver):
    def save(self, channel_id: str, content: str, destination: str):
        """
        Сохраняет переданный контент в файл в формате JSON.
        :param channel_id: ID канала.
        :param content: Текст, который нужно сохранить (будет преобразован в словарь).
        :param destination: Путь к файлу, в который нужно сохранить контент.
        """
        try:
            # Преобразуем строку в словарь
            content_dict = {
                "channel": channel_id,
                "description": content,
                "saved_at": datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            }

            os.makedirs(os.path.dirname(destination), exist_ok=True)

            # Если файл существует, откроем его и загрузим данные
            if os.path.exists(destination):
                with open(destination, 'r', encoding='utf-8') as file:
                    try:
                        existing_data = json.load(file)
                        # Убедимся, что existing_data является списком
                        if not isinstance(existing_data, list):
                            existing_data = []
                    except json.JSONDecodeError:  # Если файл пуст или поврежден, создаем пустой список
                        existing_data = []
            else:
                existing_data = []

            # Добавляем новый элемент
            existing_data.append(content_dict)

            # Перезаписываем файл с обновленными данными
            with open(destination, 'w', encoding='utf-8') as file:
                json.dump(existing_data, file, ensure_ascii=False, indent=4)

            logger.info(f"Результат обработки запроса успешно сохранен в файл: {destination}")
        except Exception as e:
            logger.error(f"Ошибка при сохранении данных в файл {destination}: {str(e)}")
            raise e
