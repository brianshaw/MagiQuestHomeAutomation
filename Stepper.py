import time
import asyncio
import threading

class Stepper:
    def __init__(self, steps, step_wait_time, end_timer_reset, step_methods, reset_method=None, end_step_called=None):
        self.steps = steps  # Total number of steps
        self.current_step = 0  # Current step index
        self.step_wait_time = step_wait_time  # Time to wait between steps
        self.end_timer_reset = end_timer_reset  # Time to wait before resetting
        self.last_step_time = time.time()  # Track last step execution time
        self.step_methods = step_methods  # List of step method functions
        self.reset_method = reset_method
        self.end_step_called = end_step_called

    async def execute_step(self):
        current_time = time.time()

        if self.current_step < self.steps:
            if self.current_step == 0 or (current_time - self.last_step_time >= self.step_wait_time):
                # Execute the step method based on current_step index
                method = self.step_methods[self.current_step]
                if method:
                    print(f"Executing {method.__name__}...")
                    await method()  # Await the method call
                
                self.last_step_time = current_time  # Update last step execution time
                self.current_step += 1  # Increment to the next step

                
                # # Start a timer to call end_step_called
                # await asyncio.sleep(self.step_wait_time)  # Wait for the step wait time
                if self.end_step_called:
                    await self.end_step_called()  # Call the end step callback if defined
                # timer = threading.Timer(self.step_wait_time, self.call_end_step_called)  # 2 seconds delay
                # timer.start()

                if self.current_step == self.steps:
                    print("All steps executed.")
                    await asyncio.sleep(self.end_timer_reset)  # Use await here
                    await self.reset()  # Reset method can be sync since it doesn't await
            else:
                print("Waiting for the next step...")
        else:
            print("All steps executed.")

    # async def call_end_step_called(self):
    #     if self.end_step_called:
    #         endcall = await self.end_step_called()
    
    async def reset(self):
        print("Resetting the stepper process...")
        self.current_step = 0
        self.last_step_time = time.time()
        # Perform cleanup tasks here
        if self.reset_method:
            await self.reset_method()  # Call the reset method if defined
        print("Stepper process reset.")

# # Example step methods
# async def step1():
#     print("Executing Step 1")
#     await asyncio.sleep(1)  # Simulate a delay for step execution

# async def step2():
#     print("Executing Step 2")
#     await asyncio.sleep(1)  # Simulate a delay for step execution

# async def step3():
#     print("Executing Step 3")
#     await asyncio.sleep(1)  # Simulate a delay for step execution

# async def end_step_callback():
#     print("End of step time reached!")

# async def main():
#     # List of methods to be executed as steps
#     step_methods = [step1, step2, step3]  # Pass function objects directly
#     end_timer_reset = 5  # Time to wait before resetting after all steps executed
#     stepper = Stepper(steps=len(step_methods), step_wait_time=2, end_timer_reset=end_timer_reset,
#                       step_methods=step_methods, end_step_called=end_step_callback)

#     print("Press 'Enter' to execute the next step (or type 'exit' to quit).")

#     while True:
#         user_input = input()  # Wait for user to press Enter
#         if user_input.lower() == 'exit':
#             print("Exiting the program.")
#             break
#         await stepper.execute_step()  # Await the execution of the step

# if __name__ == "__main__":
#     asyncio.run(main())
