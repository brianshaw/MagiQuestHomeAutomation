# from pydub import AudioSegment
# from pydub.playback import play
import subprocess
from afplay import afplay
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

# soundpath = '/Users/brianshaw/Repos/MagiQuestHomeAutomation/'
soundpath = dir_path + '/'
print(f'soundpath {soundpath}')
sounds = {
  '0': 'ding-126626.mp3',
  '1': 'mixkit-strong-close-thunder-explosion-1300.wav',
  '2': 'mixkit-rain-long-loop-2394.wav',
  '3': 'mixkit-strong-close-thunder-explosion-1300.wav',
}

def playsound(key, app='afplay'):
  # song = AudioSegment.from_mp3(f'{soundpath}{sounds[key]}')
  # song = AudioSegment.from_wav(f'{soundpath}{sounds[key]}')
  # play(song)
  # os.system(f'afplay {self.soundpath}{self.sounds[key]}')
  # return_code = subprocess.Popen(f'afplay {soundpath}{sounds[key]}', shell=True)
  # return_code = subprocess.Popen(f'mpg321 {soundpath}{sounds[key]}', shell=True)
  return_code = subprocess.Popen(f'{app} {soundpath}{sounds[key]}', shell=True)
  # return_code.kill()
  # afplay(f'{soundpath}{sounds[key]}', volume=2, time=100, leaks=True)


def test(app='afplay'):
  playsound('0', app=app)
  playsound('1', app=app)
  playsound('2', app=app)
  playsound('3', app=app)