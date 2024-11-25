import subprocess
import time

def read_dialogue():
    # Read the Arabic dialogue file
    with open('math_dialogues_arabic.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Read each line using macOS 'say' command with Arabic voice
    for line in lines:
        line = line.strip()
        if not line:  # Skip empty lines
            continue
            
        print(line)  # Print the line being read
        
        # Use macOS 'say' command with Maged voice (Arabic voice)
        try:
            subprocess.run(['say', '-v', 'Maged', line])
            time.sleep(0.2)  # Short pause between lines
        except subprocess.CalledProcessError as e:
            print(f"Error reading line: {e}")

if __name__ == "__main__":
    print("Reading dialogue using Arabic voice (Maged)...")
    read_dialogue()
