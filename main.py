import os
import sys
import asyncio
from datetime import datetime

from services.api_client import APIClient
from services.gpt_client import GPTClient
from services.logger_service import LoggerService
from services.savers.data_saver import DataSaver
from services.savers.file_saver import FileSaver

logger = LoggerService.setup_logger()


async def main(channel_id: str, limit: int = 10, save_to: str = 'file', destination: str = 'output/channel_description.json'):
    """
    Получает по ID канала его описание, генерируя его на основе аннотаций видео.
    Сохраняет результат в указанный сервис (файл или базу данных).
    :param channel_id: ID канала, для которого нужно получить описание.
    :param limit: Количество видео на канале для обработки.
    :param save_to: Место для сохранения ("file" или "db").
    :param destination: Путь к файлу или строка подключения к БД.
    :return: Краткое описание канала.
    """
    start_time = datetime.now()  # Засекаем время начала выполнения запроса
    start_time_str = start_time.strftime('%d-%m-%Y %H:%M:%S')  # Форматируем время начала
    logger.info(f"Начало обработки запроса с ID: {channel_id}, лимит: {limit}, время начала: {start_time_str}")

    try:
        api_client = APIClient()
        videos = await api_client.fetch_subtitles(channel_id, limit)

        gpt_client = GPTClient()
        result = await gpt_client.generate_channel_description(videos)

        if save_to == 'file':
            saver: DataSaver = FileSaver()
        # elif save_to == 'db':
        #     saver: DataSaver = DatabaseSaver()
        else:
            raise ValueError("Неизвестный тип сохранения! Используйте 'file' или 'db'.")

        saver.save(channel_id, result, destination)

        end_time = datetime.now()  # Засекаем время окончания выполнения запроса
        end_time_str = end_time.strftime('%d-%m-%Y %H:%M:%S')  # Форматируем время окончания
        execution_time = (end_time - start_time).total_seconds()  # Рассчитываем продолжительность в секундах
        logger.info(f"Обработка запроса завершена, время окончания: {end_time_str}, продолжительность: {execution_time:.2f} секунд.")
        return result
    except Exception as e:
        logger.error(f"Ошибка при обработке запроса: {str(e)}")
        raise


if __name__ == '__main__':
    channel_id = os.getenv('CHANNEL_ID') or (sys.argv[1] if len(sys.argv) > 1 else None)
    # limit = os.getenv('LIMIT') or (sys.argv[1] if len(sys.argv) > 1 else None)
    # save_to = os.getenv('SAVE_TO') or (sys.argv[1] if len(sys.argv) > 1 else None)
    # destination = os.getenv('DESTINATION') or (sys.argv[1] if len(sys.argv) > 1 else None)

    if not channel_id:
        raise ValueError('Не задан ID канала!')

    asyncio.run(main(channel_id))
