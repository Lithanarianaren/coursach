from gui.event.Event import Event


class Listener:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.listeners = []

    def add_listener(self, listener):
        if not isinstance(listener, Listener): return
        self.listeners.append(listener)

    def receive_event(self, event: Event):
        pass

    def send_event(self, event):
        for listener in self.listeners:
            listener.receive_event(event)
