import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os

# Initialize the speech engine
engine = pyttsx3.init()

# Function to make JARVIS speak
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Function to take voice input from the user
def take_command():
    """Listen to the user's command and return it as a string."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        return query
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError:
        print("Could not request results; check your network connection.")
        return None

def handle_disambiguation(query):
    """Handle disambiguation by allowing the user to choose from the list of options."""
    try:
        results = wikipedia.summary(query, sentences=2)
        print("According to Wikipedia: ", results)
        speak("According to Wikipedia")
        speak(results)
    except wikipedia.DisambiguationError as e:
        print(f"Your query '{query}' is ambiguous. Here are some options:")
        speak(f"Your query '{query}' is ambiguous. Here are some options:")
        for i, option in enumerate(e.options[:5]):  # Display top 5 suggestions
            print(f"{i + 1}: {option}")
            speak(f"{i + 1}: {option}")

        try:
            choice = int(input("Enter the number of the option you want to select: "))
            if 1 <= choice <= len(e.options):
                selected_option = e.options[choice - 1]
                results = wikipedia.summary(selected_option, sentences=2)
                print("According to Wikipedia: ", results)
                speak("According to Wikipedia")
                speak(results)
            else:
                print("Invalid choice.")
                speak("Invalid choice.")
        except ValueError:
            print("Please enter a valid number.")
            speak("Please enter a valid number.")
        except Exception as ex:
            print(f"An error occurred: {ex}")
            speak(f"An error occurred: {ex}")

    except wikipedia.PageError:
        print(f"No Wikipedia page found for '{query}'. Please check the query and try again.")
        speak(f"No Wikipedia page found for '{query}'. Please check the query and try again.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        speak(f"An error occurred: {e}")

def execute_jarvis():
    """Process the command and interact with Wikipedia and other functions."""
    wish_me()
    
    while True:
        query = take_command()
        if query:
            query = query.lower()
            if 'wikipedia' in query:
                speak("Searching Wikipedia...")
                query = query.replace("wikipedia", "").strip()  # Fix the syntax error
                if query:  # Check if query is not empty
                    handle_disambiguation(query)
                else:
                    speak("The Wikipedia query was empty after processing.")
                
            elif 'open youtube' in query:
                webbrowser.open("youtube.com")
                speak("Opening YouTube")

            elif 'open google' in query:
                webbrowser.open("google.com")
                speak("Opening Google")

            elif 'play music' in query:
                music_dir = 'C:\\Users\\KARTHI\\Music'
                songs = os.listdir(music_dir)
                if songs:
                    os.startfile(os.path.join(music_dir, songs[0]))
                    speak("Playing music")
                else:
                    speak("No music files found in the directory.")

            elif 'time' in query:
                str_time = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"The time is {str_time}")

            elif 'open code' in query:
                code_path = "C:\\Users\\KARTHI\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
                os.startfile(code_path)
                speak("Opening Visual Studio Code")

            elif 'exit' in query or 'quit' in query:
                speak("Goodbye!")
                break

        else:
            speak("No command detected. Please try again.")

def wish_me():
    """Wish the user based on the time of day."""
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    
    speak("I am JARVIS. How can I assist you today?")

# Run the JARVIS assistant
if __name__ == "__main__":
    execute_jarvis()
