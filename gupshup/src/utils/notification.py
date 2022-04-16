from os import path
from threading import Thread
from playsound import playsound


def notify():
    sound = path.join(path.dirname(__file__), "..", "sounds", "notification.wav")
    Thread(target=playsound, args=(sound,), daemon=True).start()
