import asyncio
import logging

import openai

from config.settings import GPT_API_KEY, GPT_CONDITION, GPT_CONDITION2, GPT_MAX_TOKENS, GPT_MODEL
from models.Video import Video
from services.text_processor import TextProcessor

logger = logging.getLogger('app_logger')


class GPTClient:
    def __init__(self):
        """
        Инициализирует клиента для работы с GPT.
        """
        self.__client = openai.OpenAI(api_key=GPT_API_KEY)
        self.__text_processor = TextProcessor()

    async def __get_summary(self, text: str, condition: str = GPT_CONDITION, assistant: str = None, **options) -> str:
        """
        Получает аннотацию чанка видео с помощью GPT.
        :param text: Текст чанка для аннотации.
        :param condition: Условие для генерации аннотации.
        :param options: Дополнительные параметры: номер элемента (el), номер чанка (n) и его тип chunk_type.
        :return: Сгенерированная аннотация.
        """
        el, n, chunk_type = options.get('el', 0) + 1, options.get('n', 0) + 1, options.get('chunk_type', 'SUBTITLES')

        logger.info(f"{chunk_type}: EL {el} - отправка {n} чанка к {GPT_MODEL} с длиной {len(text)} символов.")

        try:
            response = await asyncio.to_thread(
                self.__client.chat.completions.create,
                model=GPT_MODEL,
                messages=[
                    {"role": "system", "content": condition},
                    {"role": "user", "content": text},
                    {"role": "assistant", "content": assistant}
                ],
                max_tokens=GPT_MAX_TOKENS
            )
            logger.info(f"{chunk_type}: EL {el} - аннотация для чанка {n} успешно сгенерирована.")
            return response.choices[0].message.content.strip()

        except openai.OpenAIError as e:
            logger.error(f"Ошибка при запросе к GPT-4: {e}")
            raise Exception(f"Error GPT-4: {e}")

    async def __generate_video_annotations(self, videos: list[Video]) -> list[str]:
        """
        Генерирует аннотации для каждого видео канала на основе субтитров.
        :param videos: Список объектов Video.
        :return: Список аннотаций всех видео канала.
        """
        logger.info(f"Начало генерации аннотаций для {len(videos)} видео.")

        annotations = []
        for el, video in enumerate(videos):
            chunks = list(self.__text_processor.split(video.subtitles))

            annotation = ''
            for n, chunk in enumerate(chunks):
                try:
                    # Обновляем assistant результатом работы метода __get_summary
                    annotation = await self.__get_summary(chunk, assistant=annotation, el=el, n=n)
                except Exception as e:
                    logger.error(f"Ошибка при обработке чанка {n}: {str(e)}")
                    raise Exception(f"Ошибка при обработке чанка {n}: {str(e)}")

            annotations.append(annotation)

            # return annotations
            # self.__text_processor.save_to_file(annotation, mode='a', newline='\n')

        return annotations

    async def generate_channel_description(self, videos: list[Video]) -> str:
        """
        Генерирует краткое описание канала на основе аннотаций всех видео.
        :param videos: Список объектов Video.
        :return: Краткое описание канала.
        """
        annotations = await self.__generate_video_annotations(videos)
        logger.info(f"Генерация описания для канала из {len(annotations)} аннотаций.")

        description = ''
        for n, annotation in enumerate(annotations):
            try:
                description = await self.__get_summary(annotation, condition=GPT_CONDITION2, assistant=description, el=1, n=n, chunk_type='CHANNEL')
            except Exception as e:
                logger.error(f"Ошибка при обработке чанка {n}: {str(e)}")
                raise Exception(f"Ошибка при обработке чанка {n}: {str(e)}")

        return description
