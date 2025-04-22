from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f
from string import punctuation
from filters.chat_types import ChatTypeFilter

user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter(['group', 'supergroup']))

restricted_words = {'петян', 'кабан', 'васян'}

def clean_text(text: str):
    return text.translate(str.maketrans('', '', punctuation))  # обработчик сообщений, что заменить - на что заменить - что вырезать

@user_group_router.edited_message()
@user_group_router.message()                #ловит и удаляет сообщения со словами из списка запрещенных
async def cleaner(message: types.Message):
    if restricted_words.intersection(clean_text(message.text.lower()).split()):
        await message.answer(f'{message.from_user.first_name}, ведите себя прилично')
        await message.delete()
        await message.chat.ban(message.from_user.id)
