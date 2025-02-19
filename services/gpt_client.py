import asyncio
import logging

import openai

from config.settings import GPT_API_KEY, GPT_CONDITION, GPT_CONDITION2, GPT_CONDITION3, GPT_MAX_TOKENS, GPT_MODEL
from models.Video import Video
from services.text_processor import TextProcessor

logger = logging.getLogger('app_logger')


class GPTClient:
    def __init__(self):
        """
        Инициализирует клиента для работы с GPT.
        """
        self.client = openai.OpenAI(api_key=GPT_API_KEY)
        self.text_processor = TextProcessor()

    async def __get_summary(self, text: str, condition: str = GPT_CONDITION, **options) -> str:
        """
        Получает аннотацию чанка видео с помощью GPT.
        :param text: Текст чанка для аннотации.
        :param condition: Условие для генерации аннотации.
        :param options: Дополнительные параметры: номер элемента (el), номер чанка (n) и его тип chunk_type.
        :return: Генерированная аннотация.
        """

        el = options.get('el', 0)
        n = options.get('n', 0)
        chunk_type = options.get('chunk_type', 'SUBTITLES')

        try:
            logger.info(f"{chunk_type}: EL {el} - отправка {n} чанка к {GPT_MODEL} с длиной {len(text)} символов.")
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=GPT_MODEL,
                messages=[
                    {"role": "system", "content": condition},
                    {"role": "user", "content": text}
                ],
                max_tokens=GPT_MAX_TOKENS
            )
            logger.info(f"{chunk_type}: EL{el} - аннотация для чанка {n} успешно сгенерирована.")
            return response.choices[0].message.content.strip()
        except openai.OpenAIError as e:
            logger.error(f"Ошибка при запросе к GPT-4: {str(e)}")
            raise Exception(f"Error GPT-4: {str(e)}")

    async def __generate_video_annotations(self, videos: list[Video]) -> str:
        """
        Генерирует аннотации для видео на основе их субтитров.
        :param videos: Список объектов Video.
        :return: Аннотация к видео.
        """
        logger.info(f"Начало генерации аннотаций для {len(videos)} видео.")
        combined_text = ''

        for el, video in enumerate(videos):
            subtitle_chunks = self.text_processor.split(video.subtitles)

            logger.info(f"Разбиение субтитров видео № {el}: \"'{video.title}'\" на {len(subtitle_chunks)} чанков.")

            annotations = await asyncio.gather(
                *[self.__get_summary(chunk, GPT_CONDITION2, el=el, n=n)
                  for n, chunk in enumerate(subtitle_chunks)]
            )
            combined_text += ' '.join(annotations) + ' '

        return combined_text.strip()

    async def generate_channel_description(self, videos: list[Video]) -> str:
        """
        Генерирует краткое описание канала на основе аннотаций всех видео.
        :param videos: Список объектов Video.
        :return: Краткое описание канала.
        """

        el = 1  # Todo - в дальнейшем может быть номер канала

        video_annotations = await self.__generate_video_annotations(videos)
        annotation_chunks = self.text_processor.split(video_annotations, GPT_MAX_TOKENS)

        logger.info(f"Генерация финальной аннотации для {el} канала из {len(annotation_chunks)} чанков.")

        descriptions = await asyncio.gather(
            *[self.__get_summary(chunk, GPT_CONDITION3, el=el, n=n, chunk_type='CHANNEL')
              for n, chunk in enumerate(annotation_chunks)]
        )

        return ' '.join(descriptions).strip()
