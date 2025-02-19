from config.settings import GPT_MAX_TOKENS


class TextProcessor:
    @staticmethod
    def split(text: str, max_tokens: int = GPT_MAX_TOKENS) -> list[str]:
        """
        Разделяет текст на части, каждая из которых не превышает max_tokens.
        :param text: Текст субтитров.
        :param max_tokens: Максимальное количество токенов для одной части.
        :return: Список частей.
        """
        chunks = []
        current_chunk = []

        for word in text.split():
            if len(' '.join(current_chunk)) + len(word) + 1 > max_tokens:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
            else:
                current_chunk.append(word)

        if current_chunk:
            chunks.append(' '.join(current_chunk))

        return chunks
