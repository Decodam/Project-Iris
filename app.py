import speech_recognition as sr
import pyttsx3
import openai
from playsound import playsound
import random
import os

# Initialize the speech recognizer
r = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 170)


# Set the wake word
wake_word = "iris"

# Set up your OpenAI API key
openai.api_key = "YOUR_API_KEY_HERE"

# Set up the OpenAI response generation function
def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].text.strip()
    return message

#List of response
greetings_list = ["Hi, How can I help you?", "Hello, What can I do for you?", "Hello, How may I assist you?", "Hello there, What do you need help with?", "Greetings, Is there something I can help you with?"]
goodbyes_list = ["Thank you", "Goodbye", "Bye", "See you later", "Talk to you soon", "Until next time"]
help_offers_list = ["Is there anything else you need help with?", "Do you have any other questions?", "Is there anything I can assist you with?", "Do you need help with anything else?", "Can I help you with anything else?"]
did_not_understand_list = ["I'm sorry, I didn't understand. Could you please rephrase your question?", "I'm not sure I understand. Could you please provide more information?", "I'm sorry, I didn't catch that. Can you please repeat the question?", "I'm not sure I follow. Could you please clarify?", "I didn't quite get that. Could you please say it again?"]

# Define a function to speak the response
def speak(text):
    engine.say(text)
    engine.runAndWait()


# Define a function to listen for user input and generate responses
def listen_for_user_input():
    with sr.Microphone() as source:
        greeting = random.choice(greetings_list)
        print("Iris: ", greeting)
        speak(greeting)

        while True:
            audio = r.listen(source)
            print("Processing...")
            
            try:
                user_input = r.recognize_google(audio)
                if "terminate" in user_input.lower():
                    goodbye = random.choice(goodbyes_list)
                    print("Iris: ", goodbye)
                    speak(goodbye)
                    break
                else:
                    print("You: ", user_input)
                    prompt = f"User: {user_input}\nIris: "

                    response = generate_response(prompt)
                    print("Iris: ", response)
                    speak(response)

                    help_offer = random.choice(help_offers_list)
                    speak(help_offer)
                    print("Listening...")

            except:
                did_not_understand = random.choice(did_not_understand_list)
                print("Iris: ", did_not_understand)
                speak(did_not_understand)
                print("Listening...")


# Listen for the wake word and handle user commands
with sr.Microphone() as source:
    print("...")
    while True:
        audio = r.listen(source, 10, 3)

        try:
            text = r.recognize_google(audio)
            if wake_word in text.lower():
                playsound(f'{os.getcwd()}\sound\start.wav')
                listen_for_user_input()
                playsound(f'{os.getcwd()}\sound\end.wav')
                print("...")
        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            print("Sorry, my speech service is down.")

        
