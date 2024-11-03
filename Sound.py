# from pydub import AudioSegment
from pydub.playback import play
import subprocess

# soundpath = '/Users/brianshaw/Repos/wandcast/'
soundpath = ''
sounds = {
  '0': 'ding-sound-effect_2.mp3',
  '5': '5-monster-roar.mp3'
}

def playsound(key):
  return_code = subprocess.Popen(f'afplay {soundpath}{sounds[key]}', shell=True)


def test():
  playsound('0')