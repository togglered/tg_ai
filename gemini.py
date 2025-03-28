from openai import AsyncOpenAI, AsyncStream
from openai.types.chat import ChatCompletionChunk, ChatCompletionDeveloperMessageParam

from constants import AI_API_KEY, AI_MODEL, AI_BASE_URL

client = AsyncOpenAI(base_url=AI_BASE_URL, api_key=AI_API_KEY, )


async def send_prompt(text: str, chat: list[ChatCompletionDeveloperMessageParam]) -> AsyncStream[ChatCompletionChunk]:
    prompt = {
        "role": "user",
        "content": text
    }
    chat.append(prompt)
    stream = await client.chat.completions.create(
        model=AI_MODEL,
        messages=chat,
        stream=True,
    )
    return stream
