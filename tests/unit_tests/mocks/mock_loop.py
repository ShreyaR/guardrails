class MockLoop:
    def __init__(self, loop_is_running: bool):
        self.loop_is_running = loop_is_running
    
    def is_running(self):
        return self.loop_is_running