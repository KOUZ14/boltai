from datetime import datetime
from logging.config import listen
import speech_recognition as sr
import pyttsx3

# Speech engine initialization
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)
activationWord = 'bolt'


def speak(text, rate=170):
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()


def parseCommand():
    listener = sr.Recognizer()
    print('Listening to voice...')

    with sr.Microphone() as source:
        listener.pause_threshold = 2
        input_speech = listener.listen(source)

    try:
        print('Recognizing speech..')
        query = listener.recognize_google(input_speech, language='en')
        print(f'The input speech was: {query}')
    except Exception as exception:
        print('I did not understand what you said')
        speak('I did not understand what you said')
        
        print(exception)
        return 'None'
    
    return query

    # Main Loop
if __name__ == '__main__':
    speak('Hey Kousik!')

    while True:
        # Parse as a list
        query = parseCommand().lower().split()

        if query[0] == activationWord:
            query.pop(0)

            #List commands
            if query[0] == 'say':
                if 'hello' in query:
                    speak("Yo how's it going.")
                else:
                    query.pop(0) #remove say
                    speech = ' '.join(query)
                    speak(speech)