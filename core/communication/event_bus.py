from collections import defaultdict

class EventBus:
    def __init__(self):
        self.listeners = defaultdict(list)

    def subscribe(self, event_type: str, listener):
        self.listeners[event_type].append(listener)
        print(f"Listener subscribed to event type '{event_type}'.")

    def publish(self, event_type: str, data):
        if event_type in self.listeners:
            for listener in self.listeners[event_type]:
                listener(data)
            print(f"Event '{event_type}' published with data: {data}")
        else:
            print(f"No listeners for event type '{event_type}'.")
