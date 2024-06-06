# imports
# ---
import gradio as gr
from loguru import logger
from typing import Optional, List
from pydantic import BaseModel
from openai import AsyncOpenAI
from openai import __version__ as openai__version__

import asyncio
import os
import pickle
import platform
from datetime import datetime
from dotenv import load_dotenv


# load .env file
# ---
load_dotenv()
API_KEY = os.getenv("API_KEY")
BOT_NAME = os.getenv("BOT_NAME")
USER_NAME = os.getenv("USER_NAME")
LOAD_HISTORY = os.getenv("LOAD_HISTORY", "true").lower() == "true"

HISTORY_FILE = "chat-history.pkl"


# other code
# ---
def startup_message() -> None:
    print(r"""
 ________  ___  ___  ________  _________   
|\   ____\|\  \|\  \|\   __  \|\___   ___\ 
\ \  \___|\ \  \\\  \ \  \|\  \|___ \  \_| 
 \ \  \    \ \   __  \ \   __  \   \ \  \  
  \ \  \____\ \  \ \  \ \  \ \  \   \ \  \ 
   \ \_______\ \__\ \__\ \__\ \__\   \ \__\
    \|_______|\|__|\|__|\|__|\|__|    \|__|""")
    print(f"""
-------------------------------------------------
    Date/Time: {datetime.now()}
    Platform: {platform.platform()}
    Node: {platform.uname().node}
    Machine: {platform.uname().machine}
    Python Version: {platform.python_version()}
    Gradio Version: {gr.__version__}
    OpenAI API Version: {openai__version__}
-------------------------------------------------
                     Enjoy!
""")

async def save_chat_history_text(input_: str, response: str) -> None:
    try:
        if not os.path.isfile("chat-history.txt"):
            with open("chat-history.txt", "w", encoding="utf-8") as _file_make:
                _file_make.write(f"({datetime.now()}) File created.\n")
        with open("chat-history.txt", "a", encoding="utf-8") as file:
            file.write(f"({datetime.now()}) {BOT_NAME}: {input_}\n")
            file.write(f"({datetime.now()}) {USER_NAME}: {response}\n")
    except Exception as e:
        logger.error(f"{e}")

# code for chatbot
# ---
client = AsyncOpenAI(
    api_key=API_KEY
)

class Message(BaseModel):
    role: str
    content: str

async def make_completion(messages: List[Message], nb_retries: int = 3, delay: int = 30) -> Optional[str]:
    """
    Sends a request to the ChatGPT API to retrieve a response based on a list of previous messages.

    Parameters
    ----------
    messages : List[Message]
        A list of Message objects representing the conversation history.
    nb_retries : int, optional
        The number of retry attempts in case of failure (default is 3).
    delay : int, optional
        The delay between retry attempts in seconds (default is 30).

    Returns
    -------
    Optional[str]
        The response from the ChatGPT API, or None if the request fails.
    """
    counter = 0
    keep_loop = True
    while keep_loop:
        logger.debug(f"Chat/Completions Nb Retries : {counter}")
        try:
            chat_completion = await client.chat.completions.create(
                messages=[message.dict() for message in messages],
                model="gpt-3.5-turbo",
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            logger.error(e)
            counter = counter + 1
            keep_loop = counter < nb_retries
            await asyncio.sleep(delay)
    return None

async def predict(input_: str, history: List[dict]):
    """
    Predict the response of the chatbot and complete a running list of chat history.

    Parameters
    ----------
    input : str
        The input message from the user.
    history : List[dict]
        The chat history containing messages from the user and the assistant.

    Returns
    -------
    messages : List[tuple]
        A list of message pairs (user message, assistant response) for display in the chat UI.
    history : List[dict]
        The updated chat history including the latest user input and assistant response.
    """
    history.append({"role": "user", "content": input_})
    logger.debug(f"Query: {input_}")
    response = await make_completion([Message(**msg) for msg in history])
    logger.debug(f"Response: {response}")
    await save_chat_history_text(input_, response)
    history.append({"role": "assistant", "content": response})
    messages = [(history[i]["content"], history[i+1]["content"]) for i in range(0, len(history)-1, 2)]
    save_history(history)
    return messages, history

def save_history(history: List[dict]) -> None:
    """
    Save the chat history to a file using pickle.

    Parameters
    ----------
    history : List[dict]
        The chat history to be saved.
    """
    with open(HISTORY_FILE, 'wb') as file:
        pickle.dump(history, file)
    logger.info("Chat history saved.")

def load_history() -> List[dict]:
    """
    Load the chat history from a file using pickle.

    Returns
    -------
    List[dict]
        The chat history if the file exists, otherwise an empty list.
    """
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'rb') as file:
            history = pickle.load(file)
        logger.info(f"Chat history loaded: {len(history)} items.")
        return history
    return []

startup_message()

initial_history = load_history() if LOAD_HISTORY else []


with gr.Blocks() as demo:
    logger.info("Initiatlizing Gradio app.")
    chatbot = gr.Chatbot(label=BOT_NAME)
    state = gr.State(initial_history)
    with gr.Row():
        txt = gr.Textbox(show_label=False, placeholder="Enter text and press enter")
    txt.submit(predict, [txt, state], [chatbot, state])

demo.launch(server_port=8080)
