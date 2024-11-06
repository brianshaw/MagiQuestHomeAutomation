import pigpio
import time

class MagiQuestReceiver:
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

    def __init__(self, successCallback=None):
        self.pulses = []
        self.last_tick = 0
        self.pi = pigpio.pi()
        self.successCallback = successCallback
        
        if not self.pi.connected:
            raise Exception("Failed to connect to pigpio daemon.")

        self.pi.set_mode(self.IR_PIN, pigpio.INPUT)
        self.pi.set_glitch_filter(self.IR_PIN, 100)  # Filter out noise
        self.pi.callback(self.IR_PIN, pigpio.EITHER_EDGE, self.process_signal)

    def is_within_tolerance(self, value, target):
        return abs(value - target) <= self.TOLERANCE

    def decode_pulses(self):
        i = 0
        num_pulses = len(self.pulses)
        wand_id = 0
        magnitude = 0

        expected_pulses = 2 * 2 + (32 + 16) * 2 + 1  # Start bits + data bits + stop bit
        if num_pulses < expected_pulses:
            print("Not enough pulses received.")
            return

        for _ in range(2):
            if i + 1 >= num_pulses:
                print("Incomplete start bits.")
                return
            mark = self.pulses[i]
            space = self.pulses[i + 1]
            if self.is_within_tolerance(mark, self.MAGIQUEST_ZERO_MARK) and self.is_within_tolerance(space, self.MAGIQUEST_ZERO_SPACE):
                i += 2
            else:
                print("Invalid start bit.")
                return

        for bit_index in range(32):
            if i + 1 >= num_pulses:
                print("Incomplete wand_id bits.")
                return
            mark = self.pulses[i]
            space = self.pulses[i + 1]
            if self.is_within_tolerance(mark, self.MAGIQUEST_ONE_MARK) and self.is_within_tolerance(space, self.MAGIQUEST_ONE_SPACE):
                bit = 1
            elif self.is_within_tolerance(mark, self.MAGIQUEST_ZERO_MARK) and self.is_within_tolerance(space, self.MAGIQUEST_ZERO_SPACE):
                bit = 0
            else:
                print(f"Invalid bit in wand_id at position {bit_index}.")
                return
            wand_id = (wand_id << 1) | bit
            i += 2

        for bit_index in range(16):
            if i + 1 >= num_pulses:
                print("Incomplete magnitude bits.")
                return
            mark = self.pulses[i]
            space = self.pulses[i + 1]
            if self.is_within_tolerance(mark, self.MAGIQUEST_ONE_MARK) and self.is_within_tolerance(space, self.MAGIQUEST_ONE_SPACE):
                bit = 1
            elif self.is_within_tolerance(mark, self.MAGIQUEST_ZERO_MARK) and self.is_within_tolerance(space, self.MAGIQUEST_ZERO_SPACE):
                bit = 0
            else:
                print(f"Invalid bit in magnitude at position {bit_index}.")
                return
            magnitude = (magnitude << 1) | bit
            i += 2

        if i >= num_pulses:
            print("Incomplete stop bit.")
            return
        mark = self.pulses[i]
        if self.is_within_tolerance(mark, self.MAGIQUEST_UNIT):
            print(f"Raw magnitude: 0x{magnitude:04x} ({magnitude})")
            human_readable_magnitude = magnitude * 1000 // 0xFFFF  # Scale to 0 to 1000
            print(f"Human-readable magnitude: {human_readable_magnitude}")
            print(f"Decoded wand_id: 0x{wand_id:08x}, magnitude: {magnitude:#06x} (human-readable: {human_readable_magnitude})")

            # Call the success callback if provided
            if self.successCallback:
                self.successCallback(wand_id, magnitude, human_readable_magnitude)
        else:
            print("Invalid stop bit.")

    def process_signal(self, gpio, level, tick):
        if level == pigpio.TIMEOUT:
            return

        pulse_length = pigpio.tickDiff(self.last_tick, tick)
        self.last_tick = tick

        if pulse_length > self.PULSE_THRESHOLD:
            if self.pulses:
                print("Signal ended. Decoding pulses.")
                self.decode_pulses()
                self.pulses = []
            return

        self.pulses.append(pulse_length)

    def start(self):
        print("MagiQuest receiver started. Listening for signals...")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Exiting...")
            if self.pulses:
                print("Signal ended. Decoding pulses.")
                self.decode_pulses()
        finally:
            self.pi.stop()
