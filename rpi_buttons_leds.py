import RPi.GPIO as GPIO
import time

class RpiButtonsLeds:
    LED_PIN = 18
    BUTTON_PIN = 10

    def __init__(self, buttonCallback=None, debug=False):
      self.buttonCallback = buttonCallback
      slef.setup_buttons()
      self.setup_leds()

    def setup_buttons(self):
      print('setup buttons')
    
    def setup_leds(self):
      print('setup leds')
      # Set up the GPIO pin for the LED
      GPIO.setup(self.LED_PIN, GPIO.OUT)

      try:
        # Turn on the LED
        GPIO.output(self.LED_PIN, GPIO.HIGH)
        print("LED is ON")
        time.sleep(1)  # Keep the LED on for 1 second

        # Turn off the LED
        GPIO.output(self.LED_PIN, GPIO.LOW)
        print("LED is OFF")
      finally:
        # Clean up the GPIO settings
        GPIO.cleanup()

# print('rpi')
        
# t0 = -1
# t1 = -1

# # total = t1-t0
# GPIO.setwarnings(False) # Ignore warning for now
# GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
# GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
# while True: # Run forever
#   if GPIO.input(BUTTON_PIN) == GPIO.HIGH:
#       # print("Button was pushed!")
#       if t0 == -1:
#           t0 = time.time()
#       t1 = time.time()
#       total = t1-t0
#       if (total > 0.5):
#           print(f"Button was pressed! {total}")
#   elif t0 >= 0 and GPIO.input(BUTTON_PIN) == GPIO.LOW:
#       # t1 = time.time()
#       # total = t1-t0
#       # if (total > 0.5):
#       #     print(f"Button was released! {total}")
#       t0 = -1
#       t1 = -1



