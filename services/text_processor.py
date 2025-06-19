import math
import os

import tiktoken

from config.settings import GPT_MAX_TOKENS, GPT_MODEL


class TextProcessor:
    def __init__(self, model: str = GPT_MODEL):
        """
        Инициализация TextProcessor с заданной GPT моделью.
        :param model: Название GPT модели.
        """
        self.__encoding = tiktoken.encoding_for_model(model)
        self.file_path = 'output/annotations.txt'

    def split(self, text: str) -> list[str]:
        """
        Разделяет текст на части, каждая из которых не превышает max_tokens.
        :param text: Исходный текст.
        :return: Список частей.
        """
        tokens = self.__encode(text)
        token_count = self.__token_count(text)

        if token_count <= GPT_MAX_TOKENS:
            return [text]

        pieces = self.__pieces_count(token_count)

        chunks = []
        for i in range(pieces):
            start_idx = i * GPT_MAX_TOKENS
            end_idx = (i + 1) * GPT_MAX_TOKENS

            chunks.append(self.__decode(tokens[start_idx:end_idx]))

        return chunks

    def save_to_file(self, content: str, mode: str = 'a', newline: str = '\n'):
        """
        Сохраняет содержимое в текстовый файл.
        :param content: Содержимое, которое нужно сохранить в файл.
        :param mode: Режим записи в файл ('a' - добавление, 'w' - перезапись).
        :param newline: Символ или строка, которая будет использоваться для разделения записей.
        """
        try:
            if not os.path.exists(self.file_path):
                raise FileNotFoundError(f"Файл {self.file_path} не существует.")

            if not os.access(self.file_path, os.W_OK):
                raise PermissionError(f"Нет прав на запись в файл {self.file_path}.")

            with open(self.file_path, mode=mode) as f:
                f.write(content + newline)

        except (OSError, PermissionError, FileNotFoundError) as e:
            print(f"Ошибка при работе с файлом: {e}")

    def __encode(self, text: str) -> list[int]:
        """
        Кодирует текст в список токенов.
        :param text: Текст для кодирования.
        :return: Список токенов.
        """
        return self.__encoding.encode(text)

    def __decode(self, tokens: list[int]) -> str:
        """
        Декодирует список токенов в текст.
        :param tokens: Список токенов для декодирования.
        :return: Декодированный текст.
        """
        return self.__encoding.decode(tokens)

    @staticmethod
    def __pieces_count(token_count: int) -> int:
        """
        Подсчитывает количество частей, на которые можно разбить текст,
        исходя из максимального количества токенов приходящихся на одну часть.
        :param token_count: Общее количество токенов в тексте.
        :return: Количество частей.
        """
        return math.ceil(token_count / GPT_MAX_TOKENS)

    def __token_count(self, text: str) -> int:
        """
        Подсчитывает количество GPT токенов в тексте.
        :param text: Анализируемый текст.
        :return: Количество токенов в тексте.
        """
        tokens = self.__encode(text)
        return len(tokens)
