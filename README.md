# Chat

A simple chat applicaiton (a web app) powered by OpenAI API and Gradio.

## Features

- **Chat with a bot**: Interact with the chatbot in a simple, intuitive interface.
- **Save chat history**: Optionally save chat history to a file and reload it on startup.
- **Customizable**: Configure the bot's name, user name, and whether to load history through environment variables.

## Setup

```bash
# Install `python3`, `git`, and a text editor (`nano`)
sudo apt update && sudo apt install python3 python3-pip git nano -y

# Clone the repository and cd into it
git clone "https://github.com/hirusha-adi/Chat.git"
cd ./Chat

# Install dependencies
python3 -m pip install -r requirements.txt

# Move the example env file and move it
mv .env.example .env

# edit the .env file to set the OpenAI API key and other configurations 
nano .env

# start the web app
python ./app.py
```

## Image Showcase

Web User Inrerface:
![image](https://github.com/hirusha-adi/Chat/assets/36286877/9ed52230-57f6-4e7a-a09e-37399e3d8edf)

Console Output:
![image](https://github.com/hirusha-adi/Chat/assets/36286877/e9ac7d15-560e-44a0-ba09-c8d29689b4c0)

