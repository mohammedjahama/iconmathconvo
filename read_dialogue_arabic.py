import pyttsx3
import time

def read_dialogue():
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()
    
    # Set properties
    engine.setProperty('rate', 150)    # Speed of speech
    engine.setProperty('volume', 1.0)  # Volume
    
    # Get available voices
    voices = engine.getProperty('voices')
    
    # Try to find an Arabic voice
    arabic_voice = None
    for voice in voices:
        if 'ar' in voice.languages or 'arab' in voice.name.lower():
            arabic_voice = voice.id
            break
    
    # Set Arabic voice if found, otherwise use default
    if arabic_voice:
        engine.setProperty('voice', arabic_voice)
    
    # Read the Arabic dialogue file
    with open('math_dialogues_arabic.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Read each line
    for line in lines:
        line = line.strip()
        if not line:  # Skip empty lines
            continue
            
        print(line)  # Print the line being read
        engine.say(line)
        engine.runAndWait()
        time.sleep(0.2)  # Short pause between lines

if __name__ == "__main__":
    read_dialogue()
