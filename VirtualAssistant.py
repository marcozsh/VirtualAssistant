import webbrowser
import os
import time
import pyttsx3
import speech_recognition as sr
import re
from pwn import *
from bd_functions import *


named_tuple = time.localtime()
# these 2 lines is to get the time
time_string = time.strftime("%H:%M", named_tuple)

def def_handler(sig, frame):
    print("\n\n[!] Exiting... [!]\n")
    sys.exit(1)


def get_audioENGLISH():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        record = ""
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        record = r.recognize_google(audio, language='en', show_all=True)
        return record

def speakENGLISH(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[2].id)
    engine.setProperty('rate', 160)
    engine.say(text)
    engine.runAndWait()

def setup_name(flag):
    if flag:
        if initial_setup():
            pass
        else:
            print('something gone wrong, exiting')
            sys.exit(1)
    speakENGLISH('How do you want to call me?')
    print('listening...')
    audio = get_audioENGLISH()
    name = audio['alternative'][0]['transcript'] if str(
    type(audio)) != '<class \'list\'>' else audio[0]
    print(name)
    speakENGLISH('Do you want to call me {}?'.format(name))
    print('listening...')
    audio = get_audioENGLISH()
    answer = audio['alternative'][0]['transcript'] if str(
        type(audio)) != '<class \'list\'>' else audio[0]
    if 'yes' in answer.lower():
        set_name(name, flag)
        speakENGLISH('My name have been set, to call me you just need to say my name')
        speakENGLISH('My name is {}'.format(name))


# Ctrl+C
signal.signal(signal.SIGINT, def_handler)

name_exists = get_name()[1] # true if is not the first run
WAKE_STATUS = True if name_exists else False

if __name__ == '__main__':
    if not WAKE_STATUS: #if is the first run
        speakENGLISH('Hi, I am your Virtual Assistant. First of all, I have to do some configurations.')
        speakENGLISH('This may take a few moments')
        print('Starting configurations')
        setup_name(True)

    print('\n{}\n'.format(time_string))
    contador = 0
    while (True):
        print("listening....... \n")
        WAKE = get_name()[0]
        record = get_audioENGLISH()
        recorded_audio = str(record.count(WAKE)) if str(
            type(record)) == '<class \'list\'>' else record['alternative'][0]['transcript']
        print(str(recorded_audio))
        while True:
            if 'thank you' in recorded_audio or 'thanks' in recorded_audio:
                speakENGLISH(get_phrases(1)[random.randrange(0, len(get_phrases(1)))])
                break
            elif WAKE in recorded_audio or recorded_audio == "1":
                if contador == 0:
                    speakENGLISH(
                        "I'm {} your assistend, what can I help you?".format(WAKE))
                    contador += 1
                    break
                elif contador > 0:
                    speakENGLISH(get_phrases(2))
                    break
                else:
                    speakENGLISH("sorry, I can't understand you said")
                    break
            else:
                break

        while WAKE in recorded_audio and contador > 0:
            print("waiting orders.......")
            command = get_audioENGLISH()
            command = str(command.count(WAKE)) if str(
                type(command)) == '<class \'list\'>' else command['alternative'][0]['transcript']
            print(command)
            if "time" in command:
                speakENGLISH("it is " + time_string)
                break

            elif "purpose" in command:
                speakENGLISH(
                    "my purpose is to dominate the world and make cookies")
                break

            elif "turn off" in command:
                speakENGLISH("shutting down the computer, good night")
                sleep(3)
                os.system('shutdown /s /t 0')

            elif "search" in command:
                url = "https://www.google.cl/search?q="  # searching in google
                # capturing the words next to 'h'
                search = re.findall('search.*', command)
                search = search[0].split('search')[1]
                webbrowser.open_new_tab((url+search).strip())

                speakENGLISH(
                    "This is what i found in google for"+search)
                break
            elif "can i change your name" in command.lower():
                speakENGLISH('Yes, you can change my name any time you want')
                speakENGLISH('To change my name you need to say: {}, change your name'.format(WAKE))
                break
            elif "{} change your name".format(WAKE) in command:
                setup_name(False)
                break


