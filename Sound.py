import asyncio
import os

# Define the directory path
dir_path = os.path.dirname(os.path.realpath(__file__))
soundpath = dir_path + '/sounds/'
print(f'soundpath {soundpath}')

# Dictionary of sounds
sounds = {
    '0': 'ding-126626.mp3',
    '1': 'mixkit-strong-close-thunder-explosion-1300.mp3',
    '2': 'mixkit-rain-long-loop-2394.mp3',
    '3': 'mixkit-strong-close-thunder-explosion-1300.mp3',
    '4': 'AUDIO_8540.mp3',
}

# Asynchronous function to play sound
async def playsound(key, app='afplay'):
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
