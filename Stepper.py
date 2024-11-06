import time

class Stepper:
    def __init__(self, steps, step_wait_time, end_timer_reset, step_methods):
        self.steps = steps  # Total number of steps
        self.current_step = 0  # Current step index
        self.step_wait_time = step_wait_time  # Time to wait between steps
        self.end_timer_reset = end_timer_reset  # Time to wait before resetting
        self.last_step_time = time.time()  # Track last step execution time
        self.step_methods = step_methods  # List of step method functions

    def execute_step(self):
        if self.current_step < self.steps:
            current_time = time.time()
            if current_time - self.last_step_time >= self.step_wait_time:
                # Execute the step method based on current_step index
                method = self.step_methods[self.current_step]
                if method:
                    print(f"Executing {method.__name__}...")
                    method()  # Call the method directly
                else:
                    print("Method not found.")
                
                self.last_step_time = current_time  # Update last step execution time
                self.current_step += 1  # Increment to the next step
            else:
                print("Waiting for the next step...")
        else:
            print("All steps executed.")
            time.sleep(self.end_timer_reset)  # Wait before resetting
            self.reset()  # Call the reset method

    def reset(self):
        print("Resetting the stepper process...")
        self.current_step = 0
        self.last_step_time = time.time()
        # Perform cleanup tasks here
        print("Stepper process reset.")