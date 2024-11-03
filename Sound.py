# from pydub import AudioSegment
# from pydub.playback import play
# import subprocess
from afplay import afplay
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

# soundpath = '/Users/brianshaw/Repos/MagiQuestHomeAutomation/'
soundpath = dir_path + '/'
print(f'soundpath {soundpath}')
sounds = {
  '0': 'ding-126626.mp3',
  '5': '5-monster-roar.mp3'
}

def playsound(key):
  # song = AudioSegment.from_mp3(f'{soundpath}{sounds[key]}')
  # song = AudioSegment.from_wav(f'{soundpath}{sounds[key]}')
  # play(song)
  # os.system(f'afplay {self.soundpath}{self.sounds[key]}')
  # return_code = subprocess.Popen(f'afplay {soundpath}{sounds[key]}', shell=True)
  afplay(f'{soundpath}{sounds[key]}')
  # afplay(f'{soundpath}{sounds[key]}', volume=2, time=100, leaks=True)


def test():
  playsound('0')