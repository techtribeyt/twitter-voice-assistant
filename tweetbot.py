import speech_recognition as sr
import pyttsx3
import tweepy
import emoji
import json
# all available through pip

### ideas for future
# allow hashtags
# allow tagging others
# expand variety of emojis
# find a way to attach links or images using voice


def recognize_speech_from_mic(recognizer, source):
    print("\nListening...")
    audio = recognizer.listen(source)
    response = {"success": False}
    try:
        # gets text from audio using google's software
        response["transcription"] = recognizer.recognize_google(audio)
        response["success"] = True
    except:
        print("Error")
    return response

# get text function of tweet
def request_tweet(engine, recognizer, source, api):
    speak("What should your tweet say?", engine)
    while True:
        response = recognize_speech_from_mic(recognizer, source)
        if response["success"]:
            tweet_text = response["transcription"].capitalize()
            tweet_text += get_punctuation(engine, recognizer, source)
            print(tweet_text)
            
            tweet(tweet_text, api, engine)
            return
        
# actually send the tweet using twitter API
def tweet(text, api, engine):
    api.update_status(text)
    speak("Tweet sent!", engine)
    
    
# choose how to punctuate tweet    
def get_punctuation(engine, recognizer, source):
    speak("What punctuation would you like? Say period, exclamation, question mark, emoji, or none!", engine)
    while True:
        response = recognize_speech_from_mic(recognizer, source)
        if response["success"]:
            response_text = response["transcription"].lower()
            mapping = {"period": '.', "exclamation": '!', "question mark": '?', "none": ''}
            voice_output = phrase_to_output(response_text, mapping)
            if voice_output is not None: return voice_output
            if "emoji" in response_text: return ' ' + get_emoji(engine, recognizer, source)
        speak("Response unclear. Please try again.", engine)
  
    
# choose emoji for the tweet using voice commands
def get_emoji(engine, recognizer, source):
    speak("What emoji would you like? Say heart, thumbs up, or smiley face!", engine)
    while True:
        response = recognize_speech_from_mic(recognizer, source)
        if response["success"]:
            response_text = response["transcription"].lower()
            mapping = {
                "heart": emoji.emojize(":red_heart:", variant="emoji_type"),
                "thumbs up": emoji.emojize(':thumbs_up:'),
                "smiley face": emoji.emojize(':grinning_face:')
                }
            voice_output = phrase_to_output(response_text, mapping)
            if voice_output is not None: return voice_output
        speak("Response unclear. Please try again.", engine)          
 
# helper to convert voice phrase to some output (punctuation or emoji)
def phrase_to_output(text, mapping):
    for phrase, output in mapping.items():
        if phrase in text: return output
    return None

# have the computer say something to guide us
def speak(text, engine):
    engine.say(text)
    engine.runAndWait()



if __name__ == "__main__":
    print("Creating audio objects")
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    engine = pyttsx3.init()
    
    print("Twitter authentication")
    
    # create json file with your keys (or just paste them here)
    f = open("keys.txt",)
    keys = json.load(f)
    
    auth = tweepy.OAuthHandler(keys["consumer_key"], keys["consumer_secret_key"])
    auth.set_access_token(keys["access_token"], keys["access_token_secret"])
    api = tweepy.API(auth)
    
    print("Starting program")
    with microphone as source:
        # allows for better audio pickup
        recognizer.adjust_for_ambient_noise(source)
        while True:
            response = recognize_speech_from_mic(recognizer, source)
            if response["success"]:
                text = response["transcription"].lower()
                print(text)
                
                # key phrase to trigger tweet process
                if "send a tweet" in text:
                    request_tweet(engine, recognizer, source, api)
                elif "stop" in text:
                    break
                
