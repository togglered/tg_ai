import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode, ContentType
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from openai import AsyncStream
from openai.types.chat import ChatCompletionDeveloperMessageParam, ChatCompletionChunk
from telegramify_markdown import customize
import telegramify_markdown

from constants import TG_BOT_TOKEN
from gemini import send_prompt

customize.markdown_symbol.head_level_1 = "📌"
customize.markdown_symbol.head_level_2 = "📌"
customize.markdown_symbol.link = "🔗"
customize.strict_markdown = True
customize.cite_expandable = True

dp = Dispatcher()

all_chats: dict[int, list[ChatCompletionDeveloperMessageParam]] = {}


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("Привет!")

@dp.message(Command("clear"))
async def command_clear_handler(message: Message):
    all_chats[message.chat.id] = []
    await message.answer("🧹 История диалога очищена.")
    logging.info(all_chats)

@dp.message()
async def message_handler(message: Message) -> None:
    if message.content_type != ContentType.TEXT:
        await message.answer("Я понимаю только текстовые сообщения!")
        return

    if not all_chats.__contains__(message.chat.id):
        all_chats[message.chat.id] = []

    chat = all_chats[message.chat.id]

    temp_message = await message.answer(text="🔍 Ожидание ответа...")
    stream: AsyncStream[ChatCompletionChunk] = await send_prompt(message.text, chat)
    stream_text = ""
    try:
        async for chunk in stream:
            stream_text += chunk.choices[0].delta.content
            converted = telegramify_markdown.markdownify(stream_text)
            if len(stream_text) > 4096:
                stream_text = chunk.choices[0].delta.content
                converted = telegramify_markdown.markdownify(stream_text)
                temp_message = await temp_message.answer(text=converted, parse_mode=ParseMode.MARKDOWN_V2)
                continue
            temp_message = await temp_message.edit_text(text=converted, parse_mode=ParseMode.MARKDOWN_V2)
    except Exception as e:
        logging.error(e)
        if e.__str__() == "Provider returned error":
            await temp_message.edit_text(text="Ошибка запроса 😒! Повторите попытку позже или измените вопрос.")

    chat.append(
        {
            "role": "assistant",
            "content": stream_text
        }
    )
    logging.info(chat)


async def start() -> None:
    bot = Bot(token=TG_BOT_TOKEN)
    await dp.start_polling(bot)
