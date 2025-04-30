# фильтруем события в зависимости от того, в личке или в группе бот получил сообщение, и от кого
from aiogram.filters import Filter, IS_ADMIN
from aiogram import Bot, types


class ChatTypeFilter(Filter):
    def __init__(self, chat_types: list[str]) -> None:
        self.chat_types = chat_types

    async def __call__(self, message: types.Message) -> bool: # проверяем, что тип сообщения есть в списке применимых для этого фильтра (в переменной chat_types)
        return message.chat.type in self.chat_types

class IsAdmin(Filter):
    def __init__(self, admins_list: list[int]) -> None:
        self.admins_list = admins_list

    async def __call__(self, message: types.Message) -> bool:
        return message.from_user.id in self.admins_list