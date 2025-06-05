import pyttsx3

engine = pyttsx3.init()
engine.setProperty('voice', 'russian')


def say(text):
    engine.say(text)
    engine.runAndWait()


if __name__ == '__main__':
    say('Привет, я Нова')
