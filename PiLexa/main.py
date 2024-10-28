import time
import speech_recognition as sr
import pyttsx3
import threading
import commands
import database
import checkWhatCommand
import getLists


def speak(phrase):
    print(f'Helper says: {phrase}')
    tts = pyttsx3.init()
    voice = {
        'Zira': 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0',
        'David': 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0'
    }
    tts.setProperty('rate', 135)
    tts.setProperty('volume', 1)
    tts.setProperty('voice', voice['Zira'])

    tts.say(phrase)
    tts.runAndWait()


def activate(phrase):
    for activateWord in activateWords:
        if activateWord in phrase:
            return True
    return False


def processSpeech(words):
    try:
        words = words.split(' ')
    except AttributeError as e:
        print('No words were spoken')
        return
    # see if activated word said, if yes, have it listen again to process
    if activate(words):
        print("Python activated!")
        words = getPhrase(activated=True)
        words = words.replace(':', "")
        words = words.split(' ')
        try:
            roomAvailabilityCommand, buildingCode, day, room = checkWhatCommand.seeIfRoomAvailabilityCommand(words, days, buildingMappings, buildings, ncMappings, rooms)
        except Exception:
            roomAvailabilityCommand = False
        if roomAvailabilityCommand:
            speak(commands.command_getRoomAvailability(dbCursor, buildingCode, day, room))
        elif checkWhatCommand.seeIfFanCommand(words):
            thread = threading.Thread(target=commands.command_sendFanControl, args=([commands.extractFanCommand(words, fanModes)]))
            thread.start()
        elif checkWhatCommand.seeIfLunchCommand(words):
            speak(commands.command_getWhatsForLunch(words, days))
        elif checkWhatCommand.seeIfAzureSync(words):
            speak(commands.command_syncAzure())
        elif checkWhatCommand.seeIfMikeTeachingCommand(words):
            speak(commands.command_whenMikeTeaches(cursor=dbCursor, day=checkWhatCommand.extractDay(words, days)))
        elif checkWhatCommand.seeIfWeather(words):
            speak(commands.command_getWeather())
        elif checkWhatCommand.seeIfFischer(words):
            speak(commands.command_unlockJulieFischer())
        else:
            speak("Sorry, I could not understand that")


def getPhrase(activated):
    with sr.Microphone() as mic:
        if activated:
            thread = threading.Thread(target=speak, args=(["Yes?"]))
            time.sleep(.5)
            thread.start()
            recognizer.energy_threshold = 400
            recognizer.dynamic_energy_threshold = True
            print("Say something!")                 # shut off yellow, have green led on
            audio = recognizer.listen(mic, phrase_time_limit=5)
            try:
                text = recognizer.recognize_google(audio)
                text = text.lower()
                print(f"I heard: {text}")
                return text
            except sr.exceptions.UnknownValueError as e:
                # print(recognizer.energy_threshold)
                print("Could not understand")       # shut off green, turn on red
        else:
            # print("Adjusting for ambient noise")    # have yellow led on
            # recognizer.adjust_for_ambient_noise(mic, duration=2)
            print("Say something!")  # shut off yellow, have green led on
            audio = recognizer.listen(mic)
            try:
                text = recognizer.recognize_google(audio)
                text = text.lower()
                print(f"I heard: {text}")
                return text
            except sr.exceptions.UnknownValueError as e:
                # print(recognizer.energy_threshold)
                print("Could not understand")  # shut off green, turn on red


dbConnection, dbCursor = database.connectToDatebase()
activateWords = getLists.getActivateWords()
buildings = getLists.getBuildingCodes(dbCursor)
rooms = getLists.getRoomCodes(dbCursor)
days = getLists.getDays()
fanModes = getLists.getFanModes()
buildingMappings = getLists.getBuildingMappings()
ncMappings = getLists.getNorthCampusMappings()

recognizer = sr.Recognizer()

while True:
    try:
        processSpeech(getPhrase(activated=False))
    except Exception as e:
        print(e)
    print()
