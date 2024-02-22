# Librerie per Flask
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_executor import Executor

# Backend logica di funzionamento
from backend.magnifica import Assistente


# Librerie di base
import time
from datetime import datetime
import json
import os
import sys


# Per multithreading
import threading
from threading import Thread


current_dir = os.path.dirname(os.path.abspath(__file__))


# >>> FLASK <<<

app = Flask(__name__)
assistant = None  # Crea una variabile globale per l'assistente
socketio = SocketIO(app)
executor = Executor(app)

def start_assistant():
    print("ASSISTENTE AVVIATO")
    global assistant

    if assistant is None:
        assistant = Assistente(jsonsend)

    threading.Thread(target=assistant.AssistantCoreFunction).start()
        
# >>> GESTIONE WEB SOCKET <<<

def jsonsend(testo, animazione):
    
    
    print(testo, animazione)
    data = { 
    "text": testo,
    "animation": animazione
    }
    socketio.emit("assistant_response", data)
    print("INVIATO IL JSON A FRONT-END")
    pass


@app.route('/')
def index():
    executor.submit(start_assistant)
    return render_template('index.html')


@socketio.on("connect")
def handle_connect():
    print("Client connected")


if __name__ == '__main__':
    socketio.run(app, debug=True)
    print("XXDMFPEAP")


# >>> FUNZIONAMENTO DEL PROGRAMMA <<<
    
"""


"""