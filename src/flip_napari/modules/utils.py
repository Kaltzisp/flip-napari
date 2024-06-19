import time

class Timer:
    def __init__(self, name):
        self.start_time = time.time()
        self.name = name

    def print_duration(self):
        start_time = int(self.start_time)
        end_time = int(time.time())
        minutes = (end_time - start_time) // 60
        seconds = (end_time - start_time) % 60
        elapsed_time = f"Completed {self.name} in {minutes:02}mins {seconds}secs"
        print(elapsed_time)
