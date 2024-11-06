import argparse
import kasalights
import time
import Sound
from Stepper import Stepper
from magiquest_receiver import MagiQuestReceiver


# Define step methods
def step1():
    print("Executing Step 1")
    # Perform Step 1 operations here

def step2():
    print("Executing Step 2")
    # Perform Step 2 operations here

def step3():
    print("Executing Step 3")
    # Perform Step 3 operations here

def main():
    parser = argparse.ArgumentParser()

    source_ = parser.add_argument_group(title="input source [required]")
    source_args = source_.add_mutually_exclusive_group() # (required=True)
    # source_args.add_argument(
    #     "-C", "--cam", metavar="cam_id", nargs="?", const=0,
    #     help="Camera or video capture device ID or path. [Default 0]"
    # )
    source_args.add_argument(
        "-R", "--rpi", action="store_true",
        help="Run on Raspberry Pi"
    )
    source_args.add_argument(
        "-L", "--light", action="store", type=str, nargs='?', const='plug',
        help="Test Light 'plug' (default if empty), 'strip'"
    )
    # source_args.add_argument(
    #     "-V", "--video", type=pathlib.Path, metavar="<path>",
    #     help="Path to video file"
    # )
    source_args.add_argument(
        "-T", "--test", action="store_true", default=False,
        help="test"
    )

    other_args = parser.add_argument_group(title="Output/display options")
    
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
        import asyncio
        lights = kasalights.LightControl().start()
        if args["light"] == 'strip':
            asyncio.run(lights.testStrip())
        else:
            asyncio.run(lights.test())
        exit()
    # elif args["image"]:
    if args['rpi']:
        print('rpi')
        
        t0 = -1
        t1 = -1

        # total = t1-t0
        import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
        GPIO.setwarnings(False) # Ignore warning for now
        GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
        GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
        while True: # Run forever
          if GPIO.input(10) == GPIO.HIGH:
              # print("Button was pushed!")
              if t0 == -1:
                  t0 = time.time()
              t1 = time.time()
              total = t1-t0
              if (total > 0.5):
                  print(f"Button was pressed! {total}")
          elif t0 >= 0 and GPIO.input(10) == GPIO.LOW:
              # t1 = time.time()
              # total = t1-t0
              # if (total > 0.5):
              #     print(f"Button was released! {total}")
              t0 = -1
              t1 = -1
    if args['test']:
        Sound.test()
        exit()
    
    
    # List of methods to be executed as steps
    step_methods = [step1, step2, step3]  # Pass function objects directly
    end_timer_reset = 5  # Time to wait before resetting after all steps executed
    stepper = Stepper(steps=len(step_methods), step_wait_time=2, end_timer_reset=end_timer_reset, step_methods=step_methods)

    def handle_success_callback(wand_id, magnitude, human_readable_magnitude):
      print(f"Callback invoked! Wand ID: {wand_id}, Magnitude: {magnitude}, Human-readable Magnitude: {human_readable_magnitude}")
      stepper.execute_step()
 
    receiver = MagiQuestReceiver(successCallback=handle_success_callback)
    receiver.start()
    
    # print("Press the space bar to execute the next step.")
    # try:
    #     while True:
    #       user_input = input()  # Wait for user to press Enter
    #       if user_input.lower() == 'exit':
    #           print("Exiting the program.")
    #           break
    #       stepper.execute_step()
    # except KeyboardInterrupt:
    #     print("Exiting the program.")

main()