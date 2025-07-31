import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import urllib.request
import zipfile
import json
import queue
import sounddevice as sd
import pyautogui
import pygame
import shutil
import time
from vosk import Model, KaldiRecognizer

# TODO: Set this automatically/manually with better UI
# TODO: Clean up this clutter
INPUT_DEVICE_ID = -1
MODEL_INSTALL_DIR = 'model'
VOSK_MODEL_DL_LINK = 'https://alphacephei.com/vosk/models/vosk-model-small-de-0.15.zip'
GARMIN_SIMILARS = ['gammeln', 'gaumen', 'damen', 'carmen', 'german', 'kamen', 'gar wien']
OKAYS = ['ok', 'okay']
OK_GARMIN_AUDIO_PATH = os.path.join('sounds', 'ok_garmin.mp3')
VIDEO_SPEICHERN_AUDIO_PATH = os.path.join('sounds', 'video_speichern.mp3')
# Introduces a short delay after voice command was processed
WAIT_FOR_AUDIO = True

if INPUT_DEVICE_ID < 0:
    print('You need to set your INPUT_DEVICE_ID at the start of the script. Run print_mic_ids.py to list possible mics.')
    exit(1)

similar_commands = [f'{ok} {similar}' for similar in GARMIN_SIMILARS for ok in OKAYS]

def model_name():
    return '.'.join(VOSK_MODEL_DL_LINK.split('/')[-1].split('.')[:-1])

def model_path():
    return os.path.join(MODEL_INSTALL_DIR, model_name())

def check_install():
    print('Checking for existing model install...')
    os.makedirs(MODEL_INSTALL_DIR, exist_ok=True )
    if os.path.isdir(model_path()):
        print('Model already downloaded and installed')
        return
    print('No existing install found')
    install_model()

def install_model():
    print('Installing model...')
    zip_path = model_path() + '.zip'
    urllib.request.urlretrieve(VOSK_MODEL_DL_LINK, zip_path)
    with zipfile.ZipFile(zip_path, 'r') as extract_file:
        extract_file.extractall(path=model_path())

    # Fix nested extract
    if model_name() in os.listdir(model_path()):
        shutil.move(model_path(), model_path()+'.bak')
        shutil.move(os.path.join(model_path()+'.bak', model_name()), model_path())
        os.rmdir(model_path() + '.bak')

def check_garmin(text):
    for command in similar_commands:
        if command in text:
            return True
    return False

def check_video(text):
    return 'video speichern' in text

def action_after_verification():
    # Default NVIDIA instant replay save hotkey
    pyautogui.hotkey('alt', 'f10')


if __name__ == '__main__':
    check_install()
    model = Model(model_path())
    q = queue.Queue()

    def callback(indata, frames, time, status):
        q.put(bytes(indata))

    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
            channels=1, callback=callback, device=INPUT_DEVICE_ID):
        print('Listening...')
        rec = KaldiRecognizer(model, 16000)
        garmin_flag = False
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                text = json.loads(rec.Result()).get('text', '')

                print('You said:', text)
                if check_garmin(text):
                    pygame.mixer.init()
                    pygame.mixer.music.load(OK_GARMIN_AUDIO_PATH)
                    pygame.mixer.music.play()
                    garmin_flag = True
                elif garmin_flag and check_video(text):
                    pygame.mixer.init()
                    pygame.mixer.music.load(VIDEO_SPEICHERN_AUDIO_PATH)
                    pygame.mixer.music.play()
                    if WAIT_FOR_AUDIO:
                        while pygame.mixer.music.get_busy():
                            pygame.time.Clock().tick(10)
                        time.sleep(.5)
                    action_after_verification()
                    garmin_flag = False
                else:
                    garmin_flag = False
