import argparse
import kasalights
import time
import Sound
from Stepper import Stepper
from magiquest_receiver import MagiQuestReceiver
import asyncio

import atexit

rpiButtonsLeds = None
lights = None

async def main():
  try:
    
    global rpiButtonsLeds, lights
    parser = argparse.ArgumentParser()

    source_ = parser.add_argument_group(title="input source [required]")
    source_args = source_.add_mutually_exclusive_group() # (required=True)
    # source_args.add_argument(
    #     "-C", "--cam", metavar="cam_id", nargs="?", const=0,
    #     help="Camera or video capture device ID or path. [Default 0]"
    # )
    

    other_args = parser.add_argument_group(title="Output/display options")
    
    other_args.add_argument(
        "-R", "--rpi", action="store_true",
        help="Run on Raspberry Pi"
    )
    other_args.add_argument(
        "-L", "--light", action="store", type=str, nargs='?', const='plug',
        help="Test Light 'plug' (default if empty), 'strip'"
    )
    # source_args.add_argument(
    #     "-V", "--video", type=pathlib.Path, metavar="<path>",
    #     help="Path to video file"
    # )
    other_args.add_argument(
        "-T", "--test", action="store_true", default=False,
        help="test"
    )
    other_args.add_argument(
        "-D", "--debug", action="store_true", default=False,
        help="debug mode"
    )
    other_args.add_argument(
        "-v", "--verbose", action="store_true", help="Verbose output"
    )
    # other_args.add_argument(
    #     "-T", "--test", action="store_true", default=False,
    #     help="test"
    # )
    

    args = vars(parser.parse_args())

    # print(f'args {args}')
    if args["light"]:
        # import asyncio
        lightsTest = kasalights.LightControl().start()
        if args["light"] == 'strip':
            asyncio.run(lightsTest.testStrip())
        else:
            asyncio.run(lightsTest.test())
        exit()
    # elif args["image"]:
    # if args['rpi']:
    #     print('rpi')
        
    #     t0 = -1
    #     t1 = -1

    #     # total = t1-t0
    #     import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
    #     GPIO.setwarnings(False) # Ignore warning for now
    #     GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    #     GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
    #     while True: # Run forever
    #       if GPIO.input(10) == GPIO.HIGH:
    #           # print("Button was pushed!")
    #           if t0 == -1:
    #               t0 = time.time()
    #           t1 = time.time()
    #           total = t1-t0
    #           if (total > 0.5):
    #               print(f"Button was pressed! {total}")
    #       elif t0 >= 0 and GPIO.input(10) == GPIO.LOW:
    #           # t1 = time.time()
    #           # total = t1-t0
    #           # if (total > 0.5):
    #           #     print(f"Button was released! {total}")
    #           t0 = -1
    #           t1 = -1
    if args['rpi']:
      # app='sudo aplay'
      app='mpg321'
    else:
      app='afplay'
    if args['test']:
      # Sound.test(app=app)
      await Sound.test(app=app)
      exit()
    
    if args['rpi']:
      from rpi_buttons_leds import RpiButtonsLeds
      rpiButtonsLeds = RpiButtonsLeds()

    # import asyncio
    lights = kasalights.LightControl().start()
    executingStep = False
    # asyncio.run(lights.testStrip(dur=1))
    await lights.testStrip(dur=1)
    # Define step methods
    async def step1():
        print("Start Doing Step 1")
        executingStep = True
        if args['rpi']: rpiButtonsLeds.ledOff()
        # asyncio.run(lights.testStrip())
        # asyncio.run(lights.onLight(0))
        await lights.onLight(0)
        # await Sound.playsound('1', app=app)
        Sound.playbackgroundsound('1', app=app)
        await lights.flashLight2(lightkey=1, times=5, dur=0.5)
        executingStep = False

    async def step2():
        print("Start Doing Step 2")
        executingStep = True
        if args['rpi']: rpiButtonsLeds.ledOff()
        # Perform Step 2 operations here
        # await lights.onLight(1) # working putbackin
        Sound.playbackgroundsound('2', app=app)
        # await Sound.playsound('2', app=app)
        await lights.flashLight2(lightkey=1, times=5, dur=0.5)
        executingStep = False

    async def step3():
        print("Start Doing Step 3")
        executingStep = True
        if args['rpi']: rpiButtonsLeds.ledOff()
        Sound.playbackgroundsound('3', app=app)
        # await Sound.playsound('3', app=app)
        await lights.flashLight2(lightkey=1, times=5, dur=0.5)
        executingStep = False
    
    async def step4():
        print("Start Doing Step 4")
        executingStep = True
        if args['rpi']: rpiButtonsLeds.ledOff()
        # Perform Step 3 operations here
        # asyncio.run(lights.onLight(2))
        await lights.onLight(2)
        Sound.playbackgroundsound('4', app=app)
        await asyncio.sleep(3)
        await lights.flashLight2(lightkey=1, times=5, dur=0.5)
        await Sound.playsound('5', app=app)
        executingStep = False

    async def reset_method_callback():
        print("reset_method_callback")
        executingStep = True
        # Perform cleanup tasks here
        await lights.resetLightStrip()
        print("reset_method_callback cleandup done")
        if args['rpi']: rpiButtonsLeds.ledOn()
        executingStep = False
        Sound.playbackgroundsound('bg1', app=app, vol=20)

    async def end_step_called():
       print("end_step_called waiting")
       await asyncio.sleep(4)
       print("end_step_called continueing")
       if args['rpi']: rpiButtonsLeds.ledOn()
       await lights.onLight2(1)
    # List of methods to be executed as steps
    step_methods = [step1, step2, step3, step4]  # Pass function objects directly
    end_timer_reset = 7  # Time to wait before resetting after all steps executed
    stepper = Stepper(
       steps=len(step_methods),
       step_wait_time=10,
       end_timer_reset=end_timer_reset,
       step_methods=step_methods,
       reset_method=reset_method_callback,
       end_step_called=end_step_called
    )

    async def handle_success_callback(wand_id, magnitude, human_readable_magnitude):
      if executingStep:
        print(f"executingStep - Callback NOT invoked! Wand ID: {wand_id}, Magnitude: {magnitude}, Human-readable Magnitude: {human_readable_magnitude}")
        return
      print(f"Callback invoked! Wand ID: {wand_id}, Magnitude: {magnitude}, Human-readable Magnitude: {human_readable_magnitude}")
      await stepper.execute_step()
    
    debug=False
    if args['debug']:
        debug=True
    
    Sound.playbackgroundsound('bg1', app=app, vol=20)

    if args['rpi']:
      receiver = MagiQuestReceiver(successCallback=handle_success_callback, debug=debug)
      # from rpi_buttons_leds import RpiButtonsLeds
      # rpiButtonsLeds = RpiButtonsLeds()
      rpiButtonsLeds.ledOn()
      await receiver.start()
      
    else:
      print("Press the space bar to execute the next step.")
      try:
          while True:
            user_input = input()  # Wait for user to press Enter
            if user_input.lower() == 'exit':
                print("Exiting the program.")
                break
            await stepper.execute_step()
      except KeyboardInterrupt:
          print("Exiting the program.")
          Sound.killall()
  finally:
      # Ensure cleanup is called before exit
      await cleanup()


async def cleanup():
    global rpiButtonsLeds, lights
    print('Cleaning up...')
    if rpiButtonsLeds:
        print('Cleaning up RpiButtonsLeds...')
        rpiButtonsLeds.ledOff()
    if lights:
        print('Cleaning up LightControl...')
        try:
            await lights.resetLightStrip()
        except RuntimeError:
            print("Event loop is closed. Skipping async cleanup.")

# def exit_handler():
#     loop = asyncio.get_event_loop()
#     if loop.is_running():
#         asyncio.run_coroutine_threadsafe(cleanup(), loop)
#     else:
#         print("Event loop is not running, skipping async cleanup.")

# atexit.register(exit_handler)


# main()
# asyncio.run(main())


# Check if the event loop is already running
try:
    asyncio.get_running_loop()
    # If the loop is already running, just run the main function
    asyncio.ensure_future(main())
except RuntimeError:
    # No loop is running, so we can safely run it
    asyncio.run(main())