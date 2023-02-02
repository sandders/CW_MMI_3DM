import speech_recognition as sr
import pyttsx3
from deepmultilingualpunctuation import PunctuationModel

model = PunctuationModel()

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[14].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    try:
        with sr.Microphone() as source:
            listener = sr.Recognizer()
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice, )
            command = command.lower()
            command = command.replace('ice cream', 'icecream')
    except:
        pass
    return model.restore_punctuation(command)
