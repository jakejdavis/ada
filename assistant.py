# Import required modules
from sys import exit
from random import randint
from os import chdir, path, remove
import speech_recognition as sr
from gtts import gTTS
import wolframalpha
from random import choice as randchoice
from os import system as terminal
import urllib.request
import urllib.parse
from re import findall as refindall
import youtube_dl
from time import time as timestamp
import pygame.mixer


### FUNCTIONS ###


def chunks_function(l, n):
    # Seperate the list l every n strings
    # http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python
    for i in range(0, len(l), n):
        yield l[i:i + n]


def play_mp3(file):
    # Play mp3 using pygame.mixer used in say()
    pygame.mixer.init() # Initialise pygame
    pygame.mixer.music.load(file) # Load mp3 of what to play
    pygame.mixer.music.play() # Play mp3
    while pygame.mixer.music.get_busy(): # While playing mp3
        continue # Continue
    pygame.mixer.quit() # Once finished playing mp3, quit


def say(string, no_cache=False):
    # Say text, uses gTTS and play_mp3()
    chdir('audiocache') # Change directory to audiocache
    filename = string.replace(' ', '_') # Filename is string with spaces replace with underscores
    if not path.isfile(filename): # If file does not exist
        print("Downloading mp3 as I have not cached this") # Print message saying that the mp3 is being downloaded
        tts = gTTS(text=string, lang='en') # Make a new gTTS instance
        tts.save(filename) # Save speech with the file name of filename
    else: # If file does exist
        print("Aha! I've cached this!") # Print message saying that the mp3 already exists
    print("Saying " + string) # Print "Saying" followed by the speech
    play_mp3(filename) # Use play_mp3() function to play mp3
    if no_cache: # If no_cache is true
        remove(filename) # Delete filename
    chdir('..') # Change directory back


def check_lang_file(speech):
    # Check language file
    for lang_name in lang_commands: # For item in lang_commands variable
        for item in lang[lang_name]['Alternatives']: # For each item in alternartives list
            if speech in item: # If speech in item
                say(randchoice(lang[lang_name]['Responses'])) # Say response
                return True # Return true
    return False # Return false


def check_speech(speech, list):
    # Check if variable speech is in list
    for item in list: # For item in list variable
        if item in speech: # If item in speech
            return True # Return true
    return False # Return false


def get_youtube_link(search_query):
    # Get youtube url for search term
    say("Trying to find " + search_query, True) # Say trying to find and search_query
    query_string = urllib.parse.urlencode({"search_query": search_query}) # Url encode search_query
    html_content = urllib.request.urlopen(
        "http://www.youtube.com/results?" + query_string) # Get html content from search results
    search_results = refindall(
        r'href=\"\/watch\?v=(.{11})', html_content.read().decode()) # Get video urls from search results
    print("http://www.youtube.com/watch?v=" + search_results[0]) # Print url of video
    say("Found it") # Say "Found it"
    return ("http://www.youtube.com/watch?v=" + search_results[0]) # Return url of video


def play_song(search_query):
    # Play youtube song from seach term
    if not path.isfile('songcache/' + search_query): # If song is not cached
        url = get_youtube_link(search_query) # Get video url from get_youtube_link()
        cur_time = str(timestamp()) # Get current time and set it to cur_time
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': search_query
        } # Set youtube_dl options
        with youtube_dl.YoutubeDL(ydl_opts) as ydl: # With youtube_dl instance as ydl
            say("Downloading song") # Say "Downloading song"
            chdir('songcache') # Change directory to songcache
            ydl.download([url]) # Download mp3
    else: # If song does exist
        chdir('songcache') # Change directory to songcache
    say("Playing song") # Say playing song
    terminal("cvlc --play-and-exit --vout none '" + search_query + "'") # Play song using vlc
    chdir('..') # Change directory back


### INITILIZATION ##

say("Initilizing") # Say "Initilizing"

# LANGAUGE INIT #
say("Setting up my language index") # Say "Setting up my language index"
r = sr.Recognizer() # Create new Recongizer instance and set it to r
x = open('eng.lang', 'r').read().splitlines() # set x to eng.lang (the language file)
lang = {} # Set lang to empty dictionary
lang_commands = [] # Set lang_commands to empty list
chunks = chunks_function(x, 3) # Declare chunks variable to chunkify list every 3 items
for chunk in chunks: # For chunk in chunks
    command = chunk[0][9:] # Set command to command text
    alternatives = chunk[1].replace("alternatives: ", "").split(', ') # Set alternatives variable to alternatives string, then split alternatives up with a comma
    responses = chunk[2].replace("responses: ", "").split(', ') # Similarly, set responses variable to responses string, then split responses up with a comma

    lang_commands.append(command) # Add command to lang_command list
    lang[command] = {'Command': command,
                     'Alternatives': alternatives, 'Responses': responses} # Add command, alternatives and responses to dictionary
    print(responses) # Print responses
say("Done") # Say done

# WOLFRAM ALPHA INIT #
say("Loading AI database") # Say "Loading AI Database"
alphaclient = wolframalpha.Client('2QV77K-YQ45PUX26E') # Make new wolframalpha client
say("Done") # Say "Done"

# CALABRATION #
say("Calibrating") # say "Calibrating"
print("Calibrating", end=" ") # Print "Calibrating"
with sr.Microphone(sample_rate=22050, chunk_size=256) as source: # With microphone as source
    r.adjust_for_ambient_noise(source, duration=2.5) # Calibrate
print("done!") # Print "done!"
say("Done") # say "Done"

say("Initilizing finished")


### SPEECH RECOGNITION LOOP ###


def main(): # Main function
    while True: # While forever
        with sr.Microphone(sample_rate=22050, chunk_size=256) as source: # With microphone as source
            print("Awaiting commands!") # Print "Awaiting commands!"
            audio = r.listen(source, timeout=10) # Set variable audio to audio input
        try: # If program returns error continue
            print("Detecting...") # Print "Detecting"
            speech = r.recognize_google(audio, language="en-GB") # Recognise speech from the audio recording
            print("Speech Recognition thinks you said " + speech) # Print whay speech recgnition thinks you said
            goodbye_similar = ["goodbye", "bye", "bye-bye", "bye bye", "later"] # List of ways of saying goodbye
            speech = speech.split(" and ") # Split speech up into list seperated by the word and
            for item in speech:  # For item in speech
                if check_lang_file(item): # Check if item is in language file
                    pass # Do nothing
                elif check_speech(item, goodbye_similar): # Else if check speech in goodbye_similar list
                    say("Bye bye") # Say "Bye bye"
                    exit() # Exit program
                elif item.startswith("play "): # Else if item starts with "play"
                    song_name = item[5:] # Get song name
                    play_song(song_name) # Play song 
                elif item.startswith("answer "): # Else if item starts with "answer"
                    item = item.replace('answer ', '') # Remove answer from start
                    result = alphaclient.query(item) # Ask wolfram|alpha for answer
                    text_result = result.pods[1].text # Get answer
                    if text_result is not None: # If result not none 
                        print("Wolfram Alpha returned " + text_result) # Print what wolfram|alpha returned
                        say(text_result) # Say result
                    else: # If result is none
                        say("Wolfram Alpha Alpha doesn't know " + item) # Say "Wolfram Alpha Alpha doesn't know " & query
                else:
                    result = alphaclient.query(item) # Ask wolfram|alpha for answer
                    try:
                        text_result = result.pods[1].text
                        if text_result is not None:
                            print("Wolfram Alpha returned " + text_result)
                            say(text_result, no_cache=True)
                        else:
                            say("I don't know how to process that command")
                    except:
                        pass

        except sr.UnknownValueError: # If speech recongition cannot understand audio
            print("Google Speech Recognition could not understand audio" ) # Print error
        except sr.RequestError as e: # If there is no internet connection
            say("I think there's something up with my internet connection") # Say an error
            status = "Could not send request to Google; {0}".format(
                e) 
            print(status) # Print error

if __name__ == "__main__": # If program being run
    main() # Run main function
