import pyttsx3

def list_available_voices():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    print("Available voices:")
    print("-" * 50)
    for i, voice in enumerate(voices):
        print(f"{i+1}. ID: {voice.id}")
        print(f"   Name: {voice.name}")
        print(f"   Languages: {voice.languages}")
        print("-" * 50)

if __name__ == "__main__":
    list_available_voices()
