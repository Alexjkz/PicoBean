# PicoBean

## Introduction
PicoBean is a voice assistant meant to be integrated in a coffee machine. It is designed to run on a Raspberry Pi, plugged into a touchscreen monitor.

## Technology Used
The frontend user interface is web-based while the backend, which should run on the same machine, uses different Python modules in a flask backend, the two communicate via a WebSocket. The Python backend manages activation keyword, microphone, speech-to-text, GPT requests, text-to-speech and audio output. 
Activation keyword is managed locally to ensure quick response time, privacy, and reduced network usage. Speech-to-text and text-to-speech are done using Whisper API.
Answers are provided using a pre-defined database, or, in case no match is found for the user request, the script falls back to a ChatGPT request. Specific keywords trigger external APIs to retrieve additional informations on real-time weather and calendar.

## Getting Started
Follow this steps:
1. Download the repo
2. Install the dependencies from requirements.txt (possibly using a Venv)
3. Run the main.py script
4. Open a browser on 127.0.0.1:5000

## Technology drill-down
The following image provides detailed insight in the structure.

![PicoBean documentation (2)](https://github.com/Alexjkz/Magnifica/assets/74292381/94f97a85-729d-4c2e-8f1f-b919bb804415)

## Project team and roles
- Enrico Crosato @ichrono: JS frontend, HTTP requests, CSS animations, Calendar API.
- Alessandro Fiastri @alexjkz: Python Backend main logic, Raspberry Pi optimization and compatibility, GPT integration.
- Gianluigi Lucca Fabris @juanfabris: CSS animation, Weather API.

