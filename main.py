from datetime import datetime
from logging.config import listen
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import wolframalpha

# Speech engine initialization
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)
activationWord = 'bolt'

appId = 'HX2EHR-AXK6TARY8G'
wolframClient = wolframalpha.Client(appId)

def speak(text, rate=170):
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()

# Configure browser
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))


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

def get_first_two_sentences(text):
    sentences = text.split('. ')
    first_two = '. '.join(sentences[:2]) + '.'
    return first_two

def search_wiki(query = ''):
    searchResults = wikipedia.search(query)
    if not searchResults:
        print('No results')
        return "I couldn't find anything on that"
    try:
        wikiPage = wikipedia.page(searchResults[0])
    except wikipedia.DisambiguationError as error:
        wikiPage = wikipedia.page(error.options[0])
    print(wikiPage.title)
    wikisummary = str(wikiPage.summary)
    wikisummary = get_first_two_sentences(wikisummary)
    return wikisummary

def listOrDict(var):
    if isinstance(var, list):
        return var[0]['plaintext']
    else:
        return var['plaintext']

def search_wolframalpha(query = ''):
    response = wolframClient.query(query)
    if response['@success'] == 'false':
        return "I ain't doin this"
    else:
        result = ''
        # Question
        pod0 = response['pod'][0]
        pod1 = response['pod'][1]
        if (('result') in pod1['@title'].lower()) or (pod1.get('@primary', 'false') == 'true') or ('definition' in pod1['@title'].lower()):
            result = listOrDict(pod1['subpod'])
            return result.split('(')[0]
        else:
            # Get the interpretation from pod0
            question = listOrDict(pod0['subpod'])
            # Remove bracketed section
            question = question.split('(')[0]
            return question

    # Main Loop
if __name__ == '__main__':
    speak('Hey Kousik!')

    while True:
        # Parse as a list
        query = parseCommand().lower().split()

        if query[0] == activationWord:
            query.pop(0)

            # List commands
            if query[0] == 'say':
                if 'hello' in query:
                    speak("Yo how's it going.")
                else:
                    query.pop(0) # remove say
                    speech = ' '.join(query)
                    speak(speech)

            # Navigation
            if query[0] == 'go' and query[1]=='to':
                speak('Opening...')
                query = ' '.join(query[2:])
                webbrowser.get('chrome').open_new(query)

            # Wikepedia
            if query[0] == 'tell' and query[1] == 'me' and query[2] == 'about':
                query = ' '.join(query[2:])
                speak('Hold on let me find out.')
                result = search_wiki(query)
                speak(result)

            # Wolframalpha
            if query[0] == 'what' and query[1] == 'is':
                query = ' '.join(query[1:])
                try:
                    result = search_wolframalpha(query)
                    speak(result)
                except:
                    speak("I can't help you with this.")