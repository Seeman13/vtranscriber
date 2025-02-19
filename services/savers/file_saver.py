import logging
import os
import json
from datetime import datetime

from .data_saver import DataSaver


logger = logging.getLogger('app_logger')


class FileSaver(DataSaver):
    def save(self, content: str, destination: str):
        """
        Сохраняет переданный контент в файл в формате JSON.
        :param content: Текст, который нужно сохранить (будет преобразован в словарь).
        :param destination: Путь к файлу, в который нужно сохранить контент.
        """
        try:
            # Преобразуем строку в словарь (если это необходимо)
            content_dict = {"description": content, "saved_at": datetime.now().strftime('%d-%m-%Y %H:%M:%S')}

            os.makedirs(os.path.dirname(destination), exist_ok=True)

            # Открываем файл в режиме добавления ("a"), чтобы дописать данные
            with open(destination, 'a', encoding='utf-8') as file:
                # Если файл пустой, добавляем открывающую скобку, чтобы создать корректный JSON.
                if os.path.getsize(destination) == 0:
                    file.write('[\n')
                else:
                    file.write(',\n')
                json.dump(content_dict, file, ensure_ascii=False, indent=4)
                # Закрываем массив JSON после последнего элемента
                file.write('\n]')

            logger.info(f"Результат обработки запроса успешно сохранен в файл: {destination}")
        except Exception as e:
            logger.error(f"Ошибка при сохранении данных в файл {destination}: {str(e)}")
            raise e
