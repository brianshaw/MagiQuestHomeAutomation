import pigpio
import asyncio
import queue

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

    def __init__(self, successCallback=None, debug=False):
        self.pulses = []
        self.last_tick = 0
        self.pi = pigpio.pi()
        self.successCallback = successCallback
        self.debug = debug
        self.pulse_queue = queue.Queue()
        
        if not self.pi.connected:
            raise Exception("Failed to connect to pigpio daemon.")

        self.pi.set_mode(self.IR_PIN, pigpio.INPUT)
        self.pi.set_glitch_filter(self.IR_PIN, 100)  # Filter out noise
        self.pi.callback(self.IR_PIN, pigpio.EITHER_EDGE, self.process_signal)

    def debug_print(self, message):
        if self.debug:
            print(message)

    def is_within_tolerance(self, value, target):
        return abs(value - target) <= self.TOLERANCE

    async def decode_pulses(self):
        while not self.pulse_queue.empty():
            pulse_length = self.pulse_queue.get()
            self.pulses.append(pulse_length)

            if len(self.pulses) > 2:
                await self.process_decoding()

    async def process_decoding(self):
        i = 0
        num_pulses = len(self.pulses)
        wand_id = 0
        magnitude = 0

        expected_pulses = 2 * 2 + (32 + 16) * 2 + 1  # Start bits + data bits + stop bit
        if num_pulses < expected_pulses:
            self.debug_print("Not enough pulses received.")
            return

        # Decode start bits
        for _ in range(2):
            if i + 1 >= num_pulses:
                self.debug_print("Incomplete start bits.")
                return
            mark = self.pulses[i]
            space = self.pulses[i + 1]
            if self.is_within_tolerance(mark, self.MAGIQUEST_ZERO_MARK) and self.is_within_tolerance(space, self.MAGIQUEST_ZERO_SPACE):
                i += 2
            else:
                self.debug_print("Invalid start bit.")
                return

        # Decode wand_id
        for bit_index in range(32):
            if i + 1 >= num_pulses:
                self.debug_print("Incomplete wand_id bits.")
                return
            mark = self.pulses[i]
            space = self.pulses[i + 1]
            if self.is_within_tolerance(mark, self.MAGIQUEST_ONE_MARK) and self.is_within_tolerance(space, self.MAGIQUEST_ONE_SPACE):
                bit = 1
            elif self.is_within_tolerance(mark, self.MAGIQUEST_ZERO_MARK) and self.is_within_tolerance(space, self.MAGIQUEST_ZERO_SPACE):
                bit = 0
            else:
                self.debug_print(f"Invalid bit in wand_id at position {bit_index}.")
                return
            wand_id = (wand_id << 1) | bit
            i += 2

        # Decode magnitude
        for bit_index in range(16):
            if i + 1 >= num_pulses:
                self.debug_print("Incomplete magnitude bits.")
                return
            mark = self.pulses[i]
            space = self.pulses[i + 1]
            if self.is_within_tolerance(mark, self.MAGIQUEST_ONE_MARK) and self.is_within_tolerance(space, self.MAGIQUEST_ONE_SPACE):
                bit = 1
            elif self.is_within_tolerance(mark, self.MAGIQUEST_ZERO_MARK) and self.is_within_tolerance(space, self.MAGIQUEST_ZERO_SPACE):
                bit = 0
            else:
                self.debug_print(f"Invalid bit in magnitude at position {bit_index}.")
                return
            magnitude = (magnitude << 1) | bit
            i += 2

        if i >= num_pulses:
            self.debug_print("Incomplete stop bit.")
            return
        mark = self.pulses[i]
        if self.is_within_tolerance(mark, self.MAGIQUEST_UNIT):
            self.debug_print(f"Raw magnitude: 0x{magnitude:04x} ({magnitude})")
            human_readable_magnitude = magnitude * 1000 // 0xFFFF  # Scale to 0 to 1000
            self.debug_print(f"Human-readable magnitude: {human_readable_magnitude}")
            self.debug_print(f"Decoded wand_id: 0x{wand_id:08x}, magnitude: {magnitude:#06x} (human-readable: {human_readable_magnitude})")

            # Call the success callback if provided
            if self.successCallback:
                await self.successCallback(wand_id, magnitude, human_readable_magnitude)
        else:
            self.debug_print("Invalid stop bit.")

    def process_signal(self, gpio, level, tick):
        if level == pigpio.TIMEOUT:
            return

        pulse_length = pigpio.tickDiff(self.last_tick, tick)
        self.last_tick = tick

        if pulse_length > self.PULSE_THRESHOLD:
            if self.pulses:
                self.debug_print("Signal ended. Decoding pulses.")
                self.pulses.clear()  # Clear previous pulses if any
            return

        # Add pulse length to the queue for processing in the main loop
        self.pulse_queue.put(pulse_length)

    async def start(self):
        print("MagiQuest receiver started. Listening for signals...")  # Always print this message
        try:
            while True:
                await self.decode_pulses()  # Process the queue for pulses
                await asyncio.sleep(0.1)  # Check for new pulses periodically
        except KeyboardInterrupt:
            print("Exiting...")  # Always print this message
            if self.pulses:
                self.debug_print("Signal ended. Decoding pulses.")
                await self.decode_pulses()
        finally:
            self.pi.stop()

# # Example usage
# async def success_callback(wand_id, magnitude, human_readable_magnitude):
#     print(f"Received wand ID: {wand_id}, magnitude: {magnitude}, human-readable magnitude: {human_readable_magnitude}")

# if __name__ == "__main__":
#     receiver = MagiQuestReceiver(successCallback=success_callback, debug=True)
#     try:
#         asyncio.run(receiver.start())
#     except Exception as e:
#         print(f"Error: {e}")
