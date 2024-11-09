import asyncio
import os
import signal
import subprocess
import threading


# The os.setsid() is passed in the argument preexec_fn so
# it's run after the fork() and before  exec() to run the shell.

pro = None
proRain = None
proAmbient = None

# Define the directory path
dir_path = os.path.dirname(os.path.realpath(__file__))
soundpath = dir_path + '/sounds/'
print(f'soundpath {soundpath}')

# Dictionary of sounds
sounds = {
    '0': 'ding-126626.mp3',
    '1': 'mixkit-wind-blowing-ambience-2658.mp3',
    '2': 'mixkit-rain-long-loop-2394.mp3',
    '3': 'mixkit-strong-close-thunder-explosion-1300.mp3',
    '4': 'mixkit-electricity-lightning-blast-2601.mp3',
    '5': 'AUDIO_8540small.mp3',
    'bg1': '43-AshHills.mp3',
    'bg2': '09-Barnabas.mp3',
}

def playbackgroundsound(key, app='afplay', vol=50):
    global pro, proRain, proAmbient
    if app == 'afplay':
        appWithVol = f'{app} -v 1'
    else:
        appWithVol = f'{app} --gain {vol}'
    if proAmbient is not None:
        killbackgroundsound(process=proAmbient)
    if pro is not None:
        killbackgroundsound(process=pro)
    if proRain is not None and key == '4':
        timer = threading.Timer(4, killRain)  # 2 seconds delay
        timer.start()
    if proRain is not None and key == '5':
        print('kill rain')
        killRain()
    # Build the command
    command = f'{appWithVol} {soundpath}{sounds[key]}'
    # command = f'{app} {soundpath}{sounds[key]}'
    # Create an asynchronous subprocess
    # process = asyncio.create_subprocess_shell(command)
    if key == 'bg1' or key == 'bg2':
        proAmbient = subprocess.Popen(f'{command} -l 0', stdout=subprocess.PIPE, 
                       shell=True, preexec_fn=os.setsid)
    if key == '2':
        proRain = subprocess.Popen(command, stdout=subprocess.PIPE, 
                       shell=True, preexec_fn=os.setsid)
    else:
        pro = subprocess.Popen(command, stdout=subprocess.PIPE, 
                           shell=True, preexec_fn=os.setsid) 

def killRain():
    killbackgroundsound(process=proRain)
def killbackgroundsound(process):
    try:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    except ProcessLookupError:
        print("Process has already terminated.")
    
    
# Asynchronous function to play sound
async def playsound(key, app='afplay'):
    if proRain is not None and key == '5':
        print('kill rain')
        killbackgroundsound(process=proRain)
    # Build the command
    command = f'{app} {soundpath}{sounds[key]}'
    # Create an asynchronous subprocess
    process = await asyncio.create_subprocess_shell(command)
    # Wait for the process to finish
    await process.wait()

# Test function to play multiple sounds asynchronously
async def test(app='afplay'):
    # Run all play sound tasks concurrently
    await asyncio.gather(
        playsound('0', app=app),
        playsound('1', app=app),
        playsound('2', app=app),
        playsound('3', app=app),
        playsound('4', app=app),
    )

# # Run the test function
# if __name__ == "__main__":
#     asyncio.run(test())
