import time

class Stopwatch:
    def __init__(self):
        self.start_time = None
        self.elapsed_time = 0.0
        self.running = False

    def start(self):
        if not self.running:
            self.start_time = time.perf_counter()
            self.running = True

    def stop(self):
        if self.running:
            end_time = time.perf_counter()
            self.elapsed_time += end_time - self.start_time
            self.running = False

    def reset(self):
        self.start_time = None
        self.elapsed_time = 0.0
        self.running = False

    def get_elapsed_time(self):
        if self.running:
            current_time = time.perf_counter()
            print(current_time - self.start_time)
            return self.elapsed_time + (current_time - self.start_time)
        return self.elapsed_time