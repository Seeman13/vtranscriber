import logging
import httpx
from config.settings import API_URL
from models.Video import Video

logger = logging.getLogger('app_logger')


class APIClient:
    @staticmethod
    async def fetch_subtitles(channel_id: str, limit: int) -> list[Video]:
        """
        Асинхронно получает субтитры видео с внешнего API.
        :param channel_id: Идентификатор канала.
        :param limit: Максимальное количество субтитров для получения.
        :return: Список объектов Video.
        """
        logger.info(f"Получение субтитров для канала: {channel_id} с лимитом {limit}")
        url = API_URL.format(channel_id=channel_id, limit=limit)
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        if response.status_code == 200:
            video_data = response.json()
            logger.info(f"Получены данные {len(video_data)} видео с субтитрами.")
            return [Video(url=video['url'], title=video['title'], subtitles=video['subtitles']) for video in video_data]

        logger.error(f"Ошибка при получении данных с API: {response.status_code}")
        response.raise_for_status()
