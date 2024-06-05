# imports
# ---
import gradio as gr

import asyncio
from loguru import logger
from typing import Optional, List
from pydantic import BaseModel

import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

# load .env file
# ---
load_dotenv()

client = AsyncOpenAI(
    api_key=os.getenv("API_KEY")
)

class Message(BaseModel):
    role: str
    content: str

async def make_completion(messages: List[Message], nb_retries: int = 3, delay: int = 30) -> Optional[str]:
    counter = 0
    keep_loop = True
    while keep_loop:
        logger.debug(f"Chat Request Retries : {counter}")
        try:
            chat_completion = await client.chat.completions.create(
                messages=[message.dict() for message in messages],
                model="gpt-3.5-turbo",
            )
            print(chat_completion.choices[0].message.content)
            return chat_completion.choices[0].message.content
        except Exception as e:
            logger.error(e)
            counter = counter + 1
            keep_loop = counter < nb_retries
            await asyncio.sleep(delay)
    return None

async def predict(input, history):
    history.append({"role": "user", "content": input})
    response = await make_completion([Message(**msg) for msg in history])
    history.append({"role": "assistant", "content": response})
    messages = [(history[i]["content"], history[i+1]["content"]) for i in range(0, len(history)-1, 2)]
    return messages, history


with gr.Blocks() as demo:
    logger.info("Starting Chat Application")
    chatbot = gr.Chatbot(label="")
    state = gr.State([])
    with gr.Row():
        txt = gr.Textbox(show_label=False, placeholder="Message ")
    txt.submit(predict, [txt, state], [chatbot, state])

demo.launch(server_port=8080)
