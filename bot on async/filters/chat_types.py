# фильтруем события в зависимости от того, в личке или в группе бот получил сообщение
from aiogram.filters import Filter
from aiogram import types


class ChatTypeFilter(Filter):
    def __init__(self, chat_types: list[str]) -> None:
        self.chat_types = chat_types

    async def __call__(self, message: types.Message) -> bool: # проверяем, что тип сообщения есть в списке применимых для этого фильтра (в переменной chat_types)
        return message.chat.type in self.chat_types