from tkinter import Tk, scrolledtext, Button, Label, Frame, PhotoImage
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia

listener = sr.Recognizer()
machine = pyttsx3.init()

def talk(text):
    machine.say(text)
    machine.runAndWait()
    text_box.insert('end', 'Assistant: ' + text + '\n')  # Display response on the UI

def input_instruction():
    global instruction
    try:
        with sr.Microphone() as origin:
            listening_label.config(text="Listening...", fg="green")  # Update label text and color
            window.update_idletasks()  # Update the UI to show the changes
            speech = listener.listen(origin)
            instruction = listener.recognize_google(speech)
            instruction = instruction.lower()
            print('User said:', instruction)
            text_box.insert('end', 'User said: ' + instruction + '\n')  # Display recognized text on the UI
    except sr.UnknownValueError:
        talk("Sorry, I couldn't understand what you said.")
        instruction = None
    except sr.RequestError:
        talk("Sorry, there was an issue with the speech recognition service.")
        instruction = None
    finally:
        listening_label.config(text="", fg="black")  # Reset label text and color
        window.update_idletasks()  # Update the UI to show the changes
    return instruction

def play_VSharan():
    instruction = input_instruction()
    if instruction:
        if "play" in instruction:
            song = instruction.replace('play', "")
            talk("Playing " + song)
            pywhatkit.playonyt(song)
        elif 'time' in instruction:
            time = datetime.datetime.now().strftime('%I:%M %p')
            talk('Current time is ' + time)
        elif 'date' in instruction:
            date = datetime.datetime.now().strftime('%d/%m/%Y')
            talk("Today's date is " + date)
        elif 'how are you' in instruction:
            talk('I am fine, how about you?')
        elif 'what is your name' in instruction:
            talk('I am Kishor\'s assistant, what can I do for you?')
        elif 'who is' in instruction:
            person = instruction.replace('who is', "")
            info = wikipedia.summary(person, 1)
            print(info)
            talk(info)
        else:
            talk('Please repeat')

# Create the main application window
window = Tk()
window.title("Voice assistant")

# Create a frame to hold the button and label
frame = Frame(window)
frame.pack(pady=10)

# Load the microphone icon image
mic_icon = PhotoImage(file="mic.PNG")  # Make sure to replace "mic_icon.png" with the path to your microphone icon image

# Create a button with the microphone icon to trigger speech recognition
start_button = Button(frame, image=mic_icon, command=play_VSharan, bd=0, highlightthickness=0, cursor="hand2")
start_button.pack(side="left", padx=10)

# Set a fixed size for the button
start_button.config(width=100, height=100)

# Create a label to show "Listening..." message
listening_label = Label(frame, text="", font=("Arial", 12))
listening_label.pack(side="left")

# Create a text box to display instructions and responses
text_box = scrolledtext.ScrolledText(window, width=50, height=10, bg="lightgray", fg="black", font=("Arial", 12))
text_box.pack(pady=10)

window.mainloop()
