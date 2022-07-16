# Chat

a simple chat applicaiton powered by Machine Learning

# Guide

1. Install `python3`, `git`, and a text editor (`nano`)
    ```bash
    sudo apt update && sudo apt install python3 python3-pip git nano -y
    ```

2. Clone the repository and cd into it
    ```bash
    git clone "https://github.com/hirusha-adi/Chat.git"
    cd ./Chat
    ```

3. Install dependencies
    ```bash
    python3 -m pip install -r requirements.txt
    ```

4. Edit the `intents.json` (optional)
    ```bash
    nano intents.json
    ```

5. Train the model
    ```bash
    python3 train.py
    ```

6. Start the Chat web server
    ```bash
    python3 app.py
    ```

