import openai
import speech_recognition as sr
import pyttsx3

# setting up the Openai AI client
openai.api_key = "Your API KEY"

# setting up the speech recognition client
r = sr.Recognizer()

def generate_response(prompt):
    response = None
    try:
        # generate response from OpenAI GPT-3
        response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=4027, n=1, stop=None, temperature=1.0,)
        
    except Exception as e:
        print(f"Error: {e}")

    return response.choices[0].text.strip()

engine = pyttsx3.init()

while True:
    # ask the user to choose text or speech input
    mode = input("Enter 1 for text input, 2 for speech recognition: ")

    # handle text input
    if mode == "1":
        user_input = input('Enter new prompt: ')
        prompt = f":{user_input}\n:"
        if 'exit' in prompt or 'quit' in prompt:
            break
        response = generate_response(prompt)
        print(response)
        engine.say(response)
        engine.runAndWait()

    # handle speech recognition
    elif mode == "2":
        try:
            with sr.Microphone() as source:
                print("Speak now...")
                audio = r.listen(source)
            prompt = r.recognize_google(audio)
            print(f"You said: {prompt}")
            prompt = f":{prompt}\nAI:"
            response = generate_response(prompt)
            if 'exit' in prompt or 'quit' in prompt:
                break
            print(response)
            engine.say(response)
            engine.runAndWait()
        except sr.UnknownValueError:
            print("Sorry, I did not understand.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
    
    else:
        print("Invalid mode, please try again.")
