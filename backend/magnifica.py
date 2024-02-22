# >>>> IMPORT LIBRERIE E CONFIGURAZIONE INIZIALE <<<<

# Librerie di base
import time
from datetime import datetime
import json
import os
import sys
import random

# Playback live
import requests
import pyaudio
import soundfile as sf
import io
import time
from pydub import AudioSegment
from pydub.playback import play

#Funzione da altri moduli
from backend.funzioni.manutenzione import *
from backend.funzioni.calendarModule import getActivities
 

# Per ChatGPT e Whisper
from openai import OpenAI
from backend.apikey import *

# Per riproduzione file text-to-speech whisper e anche effetti sonori
from playsound import playsound
from pathlib import Path

# Per multithreading
import threading
from threading import Thread

# PvPorcupine Wakeword
import pvporcupine
from pvrecorder import PvRecorder
from backend.apikey import porcupine_key
porcupine = pvporcupine.create(access_key=porcupine_key, keywords=['picovoice'])
print(pvporcupine.KEYWORDS)

# Libreria speech recognition
import speech_recognition as sr
from speech_recognition import Microphone, Recognizer, UnknownValueError

# Pyaudio
import pyaudio
p = pyaudio.PyAudio()
stream = p.open(format = pyaudio.paInt16, channels = 1, rate = 48000, input = True) #Questa riga è da verificare
default_mic_dict = p.get_default_input_device_info()
default_mic_index = default_mic_dict["index"]
 
print(f"DEFAULT: {p.get_default_input_device_info()}")


# Variabili con path di ogni file di riferimento
current_dir = os.path.dirname(os.path.abspath(__file__))
behavior_dir = os.path.join(current_dir, "AI_behavior")
sound_dir = os.path.join(current_dir, "audio")
temp_dir = os.path.join(current_dir, "temp")

file_path_av_in = os.path.join(behavior_dir, "db_interazione.json")
file_path_av_out = os.path.join(behavior_dir, "db_risposta.json")
file_path_sound_db = os.path.join(behavior_dir, "db_suoni.json")
file_path_persona_GPT = os.path.join(behavior_dir, "_magnifica_persona.txt")
file_path_rispostaWhisper = os.path.join(temp_dir, "rispostaWhisper.mp3")
file_path_recAudio = os.path.join(temp_dir, "speech_utente.wav")

print(current_dir)


# Check microfoni
for i, device in enumerate(PvRecorder.get_available_devices()):
    print('Device %d: %s' % (i, device))

for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(
        f"Microphone with name \"{name}\" found for `Microphone(device_index={index})`")

p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    print(p.get_device_info_by_index(i))

p.terminate()



# >>>> CLASSE CON TUTTE LE FUNZIONI DELL'ASSISTENTE <<<<
class Assistente():
    """
    Gestisce logica di funzionamento delle varie componenti
    """

    # ---- FUNZIONE DI INIZIALIZZAZIONE ----

    def __init__(self, jsonsend_function):
        """
        Nel costruttore inizializzo il microfono e il ricevitore, in modo da non doverli dichiarare nel main
        Faccio tutte le operazioni di read & write qui in modo da velocizzare l'esecuzione delle altre funzioni
        Scrivendo self. prinma del nome delle variabili, le rendo "Variabili di istanza" e sono accessibili da tutte le funzioni nella classe "Assistente"
        """
        # device_index=1
        self.pvDeviceIndex = -1 # QUI
        self.source = Microphone(device_index=default_mic_index) # QUI
        self.jsonsend = jsonsend_function
        self.r = Recognizer()

        # Inizializzo le robe per GPT
        persona_txt = open(file_path_persona_GPT)
        self.GPT_system_persona = persona_txt.read()
        persona_txt.close()
        self.client = OpenAI(api_key=openai_key)

        self.messages=[
            {"role": "system", "content": self.GPT_system_persona }, 
        ]

        # Apro i file JSON
        with open(file_path_av_in, "r") as fileInterazione:
            self.db_interazione = json.load(fileInterazione)
        
        with open(file_path_av_out, "r") as fileRisposte:
            self.db_risposta = json.load(fileRisposte)
        
        with open(file_path_sound_db, "r") as fileSuoni:
            self.sound = json.load(fileSuoni)


    # ---- FUNZIONE RICHIAMATA DAL MAIN.PY ----

    def AssistantCoreFunction(self):
        """
        Questa è la funzione che viene richiamata dal main.py
        """
        self.wakewordDetection_Pv()

        # for thread in threading.enumerate():
        #     print(thread)
        # print(len(threading.enumerate()))

        

    # >>>> SEZIONE WAKEWORD <<<<
    
    def wakewordDetection_Pv(self):
        """
        Rilevamento della wakeword. Poi attiva il programma
        """
        pcm_recorder = self.get_next_audio_frame()
        print("POWER ON")

        while True:
            pcm_recorder.start()
            frame = pcm_recorder.read()
            keyword_index = porcupine.process(frame)
            if keyword_index >= 0:
                pcm_recorder.stop()
                # Thread avvia subito la logica dell'assistente
                t_logica = threading.Thread(target=self.logica_assistente)
                t_logica.start()

                # Thread avvia le azioni relative a interfaccia
                t_interfaceActions = threading.Thread(target=self.interfaceAction("--wakeword detected--","listeningMode", playsound=True))
                t_interfaceActions.start()

                t_logica.join()
                t_interfaceActions.join()

                t_interfaceEnd = threading.Thread(target=self.interfaceAction("--tutti i thread hanno terminato--","idleState"))
                t_interfaceEnd.start()
                t_interfaceEnd.join()


    def get_next_audio_frame(self):
        """
        Serve per ottenere l'audio in entrata della wakeword
        """

        recorder = PvRecorder(
            frame_length = 512,
            device_index = self.pvDeviceIndex)

        return recorder



    # >>>> SEZIONE LOGICA ASSISTENTE <<<<

    def logica_assistente(self):
        """
        Questo metodo serve per ascoltare richiesta utente
        """
        richiesta = self.input_voice_Whisper()

        risposta, animazione = self.assistente_vocale_out(self.assistente_vocale_in(richiesta))

        if (risposta =="Video_Manutenzione" ):
            t_browser = threading.Thread(target=VideoManutenzione())
            t_browser.start()
            t_browser.join()
        
        if ( risposta == "Impegni_Oggi" or risposta == "Impegni_Domani"):
            impegni = getActivities(risposta)
            risposta = ""
            if (impegni == None):
                risposta = "Non hai Impegni"
            else:
                for impegno in impegni:
                    risposta += f"{impegno}. "

        # if ( risposta == "Impegni_Domani"):
        #     impegni = getTomorrowActivities()
        #     risposta = ""
        #     for impegno in impegni:
        #         risposta += f"{impegno}. "
           

        #Se la risposta è "Play_Sound" riproduco il suono corrispondente all'animaizone, altrimenti leggo la risposta
        doPlaySound = (risposta == "Play_Sound")

        t_animazione = threading.Thread(target=self.interfaceAction(risposta, animazione, playsound = doPlaySound))
        t_animazione.start()

        if doPlaySound == False:
            t_risposta = threading.Thread(target=self.streamed_audio(risposta))
            t_risposta.start()
            t_risposta.join()

        t_animazione.join()
        


    
    # ---- FUNZIONE CRUCIALE PER INTERFACCIARSI CON L'UTENTE (Animazioni e suono) ----
    def interfaceAction(self, risposta, animazione, playsound=False):
        """
        Questo metodo gestisce tutte le azioni di interfaccia:
        - Animazioni
        - Suono
        - Print di debug
        """
        t_jsonsend = threading.Thread(target=self.jsonsend(risposta, animazione))
        t_jsonsend.start()

        if playsound == True:
            t_playsound = threading.Thread(target=self.audioPlayer(animazione))
            t_playsound.start()

        if animazione == "loadCoffee":
            time.sleep(6)


        print(f"Risposta: {risposta}, Animazione: {animazione}, Playsound: {playsound}")

        
    def assistente_vocale_in(self, richiesta_utente):
        """
        Script per ricevere input dall'assistente vocale.
        La funzione identifica se nell'input dell'utente sono presenti le keyword o key-phrases definite nel db_interazione
        In caso di match, verrà returned come output il CONCETTO associato alle keyword in questione
        In caso non vi sia match, verrà ritornata l'intera stringa pronunciata dall'utente
        """

        self.audioPlayer("listeningMode")
            
        no_match = True
        for concetto, keyword_list in self.db_interazione.items():
            for keyword in keyword_list:
                if keyword in richiesta_utente:
                    no_match = False
                    return concetto
                    
        if no_match == True:
            return richiesta_utente
        
    
    def assistente_vocale_out(self, concetto_in):
        """
        Script per definire gli output dall'assistente vocale
        Prende ad input come argomenti il concetto ritornato dalla funzione assistente_vocale_in()
        Nel caso sia un concetto pre-scripted ritorna randomicamente una delle risposte previste
        Alcuni concetti attivano anche una funzione, tra cui apertura pagina di YouTube su browser, lettura istruzioni complete da file, apertura gioco etc...
        Nel caso la funzione assistente_vocale_in() ritorni il prompt dell'utente perchè non lo ha associato a nessun concetto, questo prompt verrà girato all'AI powered by GPT
        Ritorna testo e animazione corrispondenti, e la variabile no_match che se "True" indica che la risposta è stata data con GPT
        """
        print("ADESSO TI RISPONDO...")
        no_match = True
        for concetto_db, risposta in self.db_risposta.items():
            if concetto_in == concetto_db:

                testo = risposta[0]
                animazione = risposta[1]
                no_match = False
                
        if no_match == True:
                testo = self.GPT_AI(concetto_in)
                animazione = "talkState"
            
        return testo, animazione
    


    # >>>> SEZIONE PER AUDIO <<<<

    def input_voice_Whisper(self):
        """
        Attiva il microfono e ritorna transcript -speech to text-
        """
    
        while True:
            try:
                with self.source as source:
                    print("QUI INIZIA AD AGGIUSTARSI PER AMBIENT NOISE")
                    self.r.adjust_for_ambient_noise(source, duration=0.5)
                    print("\n--In ascolto--")
                    audio_data = self.r.listen(source, timeout=4, phrase_time_limit=6)

                    with open(file_path_recAudio, "wb") as file:
                        file.write(audio_data.get_wav_data())
                    with open(file_path_recAudio, "rb") as audio_in:
                        transcript = self.client.audio.transcriptions.create(model="whisper-1", file=audio_in).text
                        print(transcript)
                        return(transcript.lower())
                    
            except UnknownValueError:
                print("Non hai detto niente")
            except Exception as e:
                print("ECCEZIONE ATTENZIONEEEE!!")
                #print(e)


    def streamed_audio(self, input_text, model='tts-1', voice='alloy'):
        start_time = time.time()
        # OpenAI API endpoint and parameters
        url = "https://api.openai.com/v1/audio/speech"
        headers = {
            "Authorization": f"Bearer {openai_key}", 
        }

        data = {
            "model": model,
            "input": input_text,
            "voice": voice,
            "response_format": "opus",
        }

        audio = pyaudio.PyAudio()

        def get_pyaudio_format(subtype):
            if subtype == 'PCM_16':
                return pyaudio.paInt16
            return pyaudio.paInt16

        with requests.post(url, headers=headers, json=data, stream=True) as response:
            if response.status_code == 200:
                buffer = io.BytesIO()
                for chunk in response.iter_content(chunk_size=4096):
                    buffer.write(chunk)
                
                buffer.seek(0)

                with sf.SoundFile(buffer, 'r') as sound_file:
                    format = get_pyaudio_format(sound_file.subtype)
                    channels = sound_file.channels
                    rate = sound_file.samplerate

                    stream = audio.open(format=format, channels=channels, rate=rate, output=True)
                    chunk_size = 1024
                    data = sound_file.read(chunk_size, dtype='int16')
                    print(f"Time to play: {time.time() - start_time} seconds")

                    while len(data) > 0:
                        stream.write(data.tobytes())
                        data = sound_file.read(chunk_size, dtype='int16')

                    stream.stop_stream()
                    stream.close()
            else:
                print(f"Error: {response.status_code} - {response.text}")

            audio.terminate()

            return f"Time to play: {time.time() - start_time} seconds"

    
    def print_and_speak_Whisper(self, phrase): #DEPRECATED
        """
        Funzione per attivare whisper e riprodurre il file -text to speech-
        """
        

        response = self.client.audio.speech.create(
            
            model="tts-1",
            voice="alloy",
            input=phrase,


        )
        # # >>>> Threaded option <<<<

        # start_time = time.time() # Start Benchmark

        # t_audio_risposta_stream = threading.Thread(target = response.stream_to_file(file_path_rispostaWhisper))
        # t_audio_risposta_stream.start()
        # #time.sleep(0.01)

        # end_time = time.time()
        # t_playback_stream = threading.Thread(target = playsound(file_path_rispostaWhisper))
        # t_playback_stream.start()

        
        # t_audio_risposta_stream.join()
        # t_playback_stream.join()

        # >>>> Non-threaded option <<<<

        start_time = time.time()

        response.stream_to_file(file_path_rispostaWhisper)

        end_time = time.time()

        playsound(file_path_rispostaWhisper)

        # >>>> Commonbench <<<<

        duration = end_time - start_time
        print(f"The code took {duration} seconds to execute")


    

    def audioPlayer(self, animazione):
        """
        Riproduce il suono corrispondente all'animazione fornita in input
        """
        print("AUDIOPLAYER")
        if animazione in self.sound:
                try:
                        audio = random.choice(self.sound[animazione])
                        audiofilepath = os.path.join(sound_dir, audio)
                        playsound(audiofilepath)
                except Exception as e:
                        print(e)
        else:
                print("Clip audio corrispondente all'animazione fornita non trovata")

    

    # >>>> SEZIONE AI GPT <<<<
            
    def GPT_AI(self, question):
        """
        Funzione per dialogo con AI GPT
        """

        self.messages.append({"role": "user", "content":question})

        my_completion = self.client.chat.completions.create(
        model = "gpt-3.5-turbo", 
        messages = self.messages,
        temperature = 0.7,
        stream = True
        )
        collected_chunks = []
        full_reply = ""

        for chunk in my_completion:
            #print(chunk.choices[0].delta.content)
            collected_chunks.append(chunk.choices[0].delta.content)

        #print(collected_chunks)
        collected_messages = [m for m in collected_chunks if m is not None]
        #print(collected_messages)
        full_reply = ''.join([m for m in collected_messages])
        #print(full_reply)


        return full_reply
        #return my_completion.choices[0].message.content
    









