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
        current_time = time.time()

        if self.current_step < self.steps:
            if current_time - self.last_step_time >= self.step_wait_time:
                # Execute the step method based on current_step index
                method = self.step_methods[self.current_step]
                if method:
                    print(f"Executing {method.__name__}...")
                    method()  # Call the method directly
                
                self.last_step_time = current_time  # Update last step execution time
                self.current_step += 1  # Increment to the next step

                if self.current_step == self.steps:
                    # If last step was executed, print "All steps executed"
                    print("All steps executed.")
                    time.sleep(self.end_timer_reset)  # Wait before resetting
                    self.reset()  # Call the reset method
            else:
                print("Waiting for the next step...")
        else:
            print("All steps executed.")  # Just in case this is called again

    def reset(self):
        print("Resetting the stepper process...")
        self.current_step = 0
        self.last_step_time = time.time()
        # Perform cleanup tasks here
        print("Stepper process reset.")

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
    # List of methods to be executed as steps
    step_methods = [step1, step2, step3]  # Pass function objects directly
    end_timer_reset = 5  # Time to wait before resetting after all steps executed
    stepper = Stepper(steps=len(step_methods), step_wait_time=2, end_timer_reset=end_timer_reset, step_methods=step_methods)

    print("Press 'Enter' to execute the next step (or type 'exit' to quit).")

    while True:
        user_input = input()  # Wait for user to press Enter
        if user_input.lower() == 'exit':
            print("Exiting the program.")
            break
        stepper.execute_step()

if __name__ == "__main__":
    main()
