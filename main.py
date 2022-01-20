import speech_recognition as sr # speech recogniton
import playsound # to play an audio file
import random # to generate random audio file name
import time
import webbrowser # open browser
import os # to remove piled audio files
import pyautogui # screenshot
import requests # web scraping

from PIL import Image # to show timetable
from gtts import gTTS  # google text to speech
from time import ctime # get current time details

class person:
    name = ''
    def setName(self, name):
        self.name = name

class alexis:
    name = ''
    def setName(self, name):
        self.name = name

def there_exists(terms):
    for term in terms:
        if term in voice_data:
            return True

r = sr.Recognizer() # initialize a recognizer

# listen for the audio and convert it to text
def record_audio(ask=False):
    with sr.Microphone() as source:  # microphone as source
        if ask:
            alexis_speak(ask)
        audio = r.listen(source) # listen for the audio via source
        print("Done Listening")
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError: # error : recognizer does not understand
            alexis_speak('Sorry, I did not get it')
        except sr.RequestError: # error : recognizer is not connected
            alexis_speak('Sorry, the service is down')
        print('User:', voice_data.lower()) # print what user said
        return voice_data.lower()

# get text or string and make an audio file to be played out of it and remove it from the pile
def alexis_speak(audio_string):
    audio_string = str(audio_string)
    tts = gTTS(text= audio_string, lang= 'en') # text to speech(voice)
    ran = random.randint(1,2000000)
    audio_file = 'audio-' + str(ran) + '.mp3'   # set audio file name in mp3 format
    tts.save(audio_file) # save file as mp3
    playsound.playsound(audio_file)  # play the audio file
    print(alexis_obj.name + ':' + audio_string)
    os.remove(audio_file) # remove audio file

# response of alexis to voice_data
def respond(voice_data):
    # 1 : Greetings
    if there_exists(['hey','hi','hello','namaste','hai']):
        greetings = ["hey, how can I help you" + person_obj.name, "hey, what's up?" + person_obj.name, "how can I help you?" + person_obj.name, "hello" + person_obj.name]
        greet = greetings[random.randint(0,len(greetings)-1)]
        alexis_speak(greet)

    if there_exists(["how are you", "how are you doing"]):
        alexis_speak("I'm very well, thanks for asking " + person_obj.name)

    # 2 : Name
    if there_exists(["what is your name","what's your name","tell me your name"]):
        if person_obj.name:
            alexis_speak(f"My name is {alexis_obj.name}, {person_obj.name}") #gets users name from voice input
        else:
            alexis_speak(f"My name is {alexis_obj.name}. what's your name?") #incase you haven't provided your name

    if there_exists(["my name is"]):
        person_name = voice_data.split("is")[-1].strip()
        alexis_speak("okay, i will remember that " + person_name)
        person_obj.setName(person_name) # remember name in person object

    if there_exists(["what is my name"]):
        alexis_speak("Your name must be " + person_obj.name)

    if there_exists(["your name should be"]):
        alexis_name = voice_data.split("be")[-1].strip()
        alexis_speak("okay, i will remember my name is " + alexis_name)
        alexis_obj.setName(alexis_name) # remember name in asis object

    # 3 : Date and Time
    if there_exists(["what's the date today", "what is the date today", "what is the date", "what's the date", "what day is it","tell me the date"]):
        day = ctime().split(" ")
        alexis_speak(day[0]+ " " + day[1] + " " + str(day[2]) + ", " + str(day[4]))

    if there_exists(["what's the time now", "what is the time now","what is the time","what's the time","what time is it","tell me the time"]):
        time = ctime().split(" ")[3].split(":")[0:2]
        hours= time[0]
        minutes = time[1]
        alexis_speak(hours+ " hours "+ minutes + " minutes ")

    # 4 : Time table
    if there_exists(["show my time table"]):
        img = Image.open(r"timetable.jpeg")
        img.show()
        alexis_speak("Here is your time table")

    # 5 : Screenshot
    if there_exists(["capture","my screen", "screenshot"]):
        ss = pyautogui.screenshot()
        ss.save('C:/Users/HP/Pictures/Screenshots/screen.png')
        alexis_speak("Screenshot has been saved in current folder")

    # 6 : rock paper scissors
    if there_exists(["let's play rock paper scissor"]):
        alexis_speak("ok! Let's play")
        voice_data = record_audio("choose among rock paper or scissor")
        moves = ["rock", "paper", "scissor"]

        cmove = random.choice(moves)
        pmove = voice_data

        alexis_speak("The computer chose " + cmove)
        alexis_speak("You chose " + pmove)

        if pmove == cmove:
            alexis_speak("the match is draw")
        elif pmove == "rock" and cmove == "scissor":
            alexis_speak("Player Wins")
        elif pmove == "rock" and cmove == "paper":
            alexis_speak("Computer Wins")
        elif pmove == "paper" and cmove == "scissor":
            alexis_speak("Computer Wins")
        elif pmove == "paper" and cmove == "rock":
            alexis_speak("Player Wins")
        elif pmove == "scissor" and cmove == "paper":
            alexis_speak("Player Wins")
        elif pmove == "scissor" and cmove == "rock":
            alexis_speak("Computer Wins")

    # 7 : Simple Calculator
    if there_exists(["plus", "minus", "multiply", "divide", "power", "+", "-", "*", "/"]):
        opr = voice_data.split()[1]

        if opr == '+':
            alexis_speak(int(voice_data.split()[0]) + int(voice_data.split()[2]))
        elif opr == '-':
            alexis_speak(int(voice_data.split()[0]) - int(voice_data.split()[2]))
        elif opr == 'multiply' or 'x':
            alexis_speak(int(voice_data.split()[0]) * int(voice_data.split()[2]))
        elif opr == 'divide':
            alexis_speak(int(voice_data.split()[0]) / int(voice_data.split()[2]))
        elif opr == 'power':
            alexis_speak(int(voice_data.split()[0]) ** int(voice_data.split()[2]))
        else:
            alexis_speak("Wrong Operator")

    # 7 : Google search
    if there_exists(["search for","google search for","search"]) and 'youtube' not in voice_data:
        search_term = voice_data.split("for")[-1]
        url = "https://google.com/search?q=" + search_term
        webbrowser.get().open(url)
        alexis_speak("Here is what I found for " + search_term + " on google")

    # 8 : Youtube search
    if there_exists(["youtube search","youtube search for","youtube"]):
        search_term = voice_data.split("for")[-1]
        url = "https://www.youtube.com/results?search_query=" + search_term
        webbrowser.get().open(url)
        alexis_speak("Here is what i found for " + search_term + " in youtube")

    # 9 : location
    # find location
    if there_exists(["find location of"]):
        location = voice_data.split("of")[-1]
        url = 'https://www.google.com/maps/place/' + location +'/&amp;'
        webbrowser.get().open(url)
        alexis_speak("Here is the location of " + location + " found on google maps")

    # Current location as per Google maps
    if there_exists(["what is my exact location"]):
        url = "https://www.google.com/maps/search/Where+am+I+?/"
        webbrowser.get().open(url)
        alexis_speak("You must be somewhere near here, as per Google maps")

    # 10 : Exit
    if there_exists(["quit", "exit", "goodbye","end"]):
        alexis_speak("bye! I am going offline")
        exit()

time.sleep(1)

person_obj = person()
alexis_obj = alexis()
alexis_obj.name = 'alexis'
person_obj.name = ''


while 1:
    voice_data = record_audio('recording') # get the voice input
    #print("Done")
    #print("User:",voice_data)
    respond(voice_data) # respond