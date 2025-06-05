import pyttsx3
from pyttsx3 import engine

engine = pyttsx3.init()
voices = engine.getProperty('voices')

idx = 0
for voice in voices:
    if voice.name == "Microsoft An - Vietnamese (Vietnam)":
        engine.setProperty('voice', voices[idx].id)
        print("Set voice to Vietnamese")
    print("Voice:")
    print(" - ID: %s" % voice.id)
    print(" - Name: %s" % voice.name)
    print(" - Languages: %s" % voice.languages)
    print(" - Gender: %s" % voice.gender)
    print(" - Age: %s" % voice.age)
    idx += 1

# engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 180)
engine.say("Xin chào, tôi là người lập trình. Tuy tôi biết lập trình nhưng tôi không lập trình! =)")
engine.runAndWait()
    