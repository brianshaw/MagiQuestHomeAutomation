import pigpio
import time

# Constants based on the MagiQuest protocol
MAGIQUEST_UNIT = 288  # microseconds
MAGIQUEST_ONE_MARK = 2 * MAGIQUEST_UNIT  # 576 us
MAGIQUEST_ONE_SPACE = 2 * MAGIQUEST_UNIT  # 576 us
MAGIQUEST_ZERO_MARK = MAGIQUEST_UNIT      # 288 us
MAGIQUEST_ZERO_SPACE = 3 * MAGIQUEST_UNIT # 864 us

# Adjusted tolerance margin
TOLERANCE = 150  # ±150 microseconds

# Pin configuration
IR_PIN = 14
PULSE_THRESHOLD = 100000  # 100 ms threshold to ignore very large pulses

# Variables to track the pulses
pulses = []
last_tick = 0

def is_within_tolerance(value, target):
    return abs(value - target) <= TOLERANCE

def decode_pulses(pulses):
    # pulses is a list of pulse lengths in microseconds
    # We need to process them in pairs (mark and space)
    i = 0
    num_pulses = len(pulses)
    wand_id = 0
    magnitude = 0

    # Check for at least enough pulses for start bits and data
    expected_pulses = 2 * 2 + (32 + 16) * 2 + 1  # Start bits + data bits + stop bit
    if num_pulses < expected_pulses:
        print("Not enough pulses received.")
        return

    # Decode start bits
    for _ in range(2):
        if i + 1 >= num_pulses:
            print("Incomplete start bits.")
            return
        mark = pulses[i]
        space = pulses[i+1]
        if is_within_tolerance(mark, MAGIQUEST_ZERO_MARK) and is_within_tolerance(space, MAGIQUEST_ZERO_SPACE):
            i += 2
        else:
            print("Invalid start bit.")
            return

    # Decode wand_id (32 bits)
    for bit_index in range(32):
        if i + 1 >= num_pulses:
            print("Incomplete wand_id bits.")
            return
        mark = pulses[i]
        space = pulses[i+1]
        if is_within_tolerance(mark, MAGIQUEST_ONE_MARK) and is_within_tolerance(space, MAGIQUEST_ONE_SPACE):
            bit = 1
        elif is_within_tolerance(mark, MAGIQUEST_ZERO_MARK) and is_within_tolerance(space, MAGIQUEST_ZERO_SPACE):
            bit = 0
        else:
            print(f"Invalid bit in wand_id at position {bit_index}.")
            return
        wand_id = (wand_id << 1) | bit
        i += 2

    # Decode magnitude (16 bits)
    for bit_index in range(16):
        if i + 1 >= num_pulses:
            print("Incomplete magnitude bits.")
            return
        mark = pulses[i]
        space = pulses[i+1]
        if is_within_tolerance(mark, MAGIQUEST_ONE_MARK) and is_within_tolerance(space, MAGIQUEST_ONE_SPACE):
            bit = 1
        elif is_within_tolerance(mark, MAGIQUEST_ZERO_MARK) and is_within_tolerance(space, MAGIQUEST_ZERO_SPACE):
            bit = 0
        else:
            print(f"Invalid bit in magnitude at position {bit_index}.")
            return
        magnitude = (magnitude << 1) | bit
        i += 2

    # Expect stop bit (MARK of UNIT length)
    if i >= num_pulses:
        print("Incomplete stop bit.")
        return
    mark = pulses[i]
    if is_within_tolerance(mark, MAGIQUEST_UNIT):
        # Raw magnitude value
        print(f"Raw magnitude: 0x{magnitude:04x} ({magnitude})")

        # Convert to human-readable number (adjust the scaling as needed)
        human_readable_magnitude = magnitude * 1000 // 0xFFFF  # Scale it to a range of 0 to 1000
        print(f"Human-readable magnitude: {human_readable_magnitude}")

        # Output the wand_id and the magnitude values
        print(f"Decoded wand_id: 0x{wand_id:08x}, magnitude: {magnitude:#06x} (human-readable: {human_readable_magnitude})")
    else:
        print("Invalid stop bit.")

def process_signal(gpio, level, tick):
    global last_tick, pulses
    if level == pigpio.TIMEOUT:
        return

    pulse_length = pigpio.tickDiff(last_tick, tick)
    last_tick = tick

    # Ignore long pulses (filter out noise)
    if pulse_length > PULSE_THRESHOLD:
        # Reset pulse collection on long gap
        if pulses:
            print("Signal ended. Decoding pulses.")
            decode_pulses(pulses)
            pulses = []
        return

    pulses.append(pulse_length)

# Setup
pi = pigpio.pi()
if not pi.connected:
    exit()

pi.set_mode(IR_PIN, pigpio.INPUT)
pi.set_glitch_filter(IR_PIN, 100)  # Filter out noise
last_tick = 0

# Set up callback for IR signal reception
pi.callback(IR_PIN, pigpio.EITHER_EDGE, process_signal)

# Keep the program running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting")
    if pulses:
        print("Signal ended. Decoding pulses.")
        decode_pulses(pulses)
finally:
    pi.stop()
