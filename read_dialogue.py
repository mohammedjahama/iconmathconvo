import pyttsx3
import time

def read_dialogue():
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()
    
    # Set properties
    engine.setProperty('rate', 150)    # Speed of speech
    engine.setProperty('volume', 1.0)  # Volume
    
    # Set Samantha's voice for all dialogue
    voices = engine.getProperty('voices')
    samantha_voice = None
    
    # Find Samantha's voice
    for voice in voices:
        if "Samantha" in voice.name:
            samantha_voice = voice.id
            break
    
    if samantha_voice:
        engine.setProperty('voice', samantha_voice)
    
    # Read the dialogue file
    with open('math_dialogues_updated.txt', 'r') as file:
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
