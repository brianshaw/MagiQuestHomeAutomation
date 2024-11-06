import RPi.GPIO as GPIO
import time

class RpiButtonsLeds:
    LED_PIN = 16
    BUTTON_PIN = 10

    def __init__(self, buttonCallback=None, debug=False):
      self.buttonCallback = buttonCallback
      self.setupGPIO()
      self.setup_buttons()
      self.setup_leds()

    def setupGPIO(self):
      GPIO.setwarnings(False) # Ignore warning for now
      GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    
    def setup_buttons(self):
      print('setup buttons')
    
    def setup_leds(self):
      print('setup leds')
      # Set up the GPIO pin for the LED
      GPIO.setup(self.LED_PIN, GPIO.OUT)
    
    def ledOn(self):
      # Turn on the LED
      GPIO.output(self.LED_PIN, GPIO.HIGH)
      print("LED is ON")
    
    def ledOff(self):
      # Turn off the LED
      GPIO.output(self.LED_PIN, GPIO.LOW)
      print("LED is OFF")
    
    def resetLed(self):
      self.ledOff()
      self.cleanup()
    def cleanup():
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


