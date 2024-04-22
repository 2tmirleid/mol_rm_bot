import sys

import os
from watchdog.events import LoggingEventHandler
from watchdog.observers import Observer


class Watcher:
    def __init__(self):
        self.path = None

        self.event_handler = LoggingEventHandler()
        self.observer = Observer()

    def watch(self):
        self.path = sys.argv[1] if len(sys.argv) > 1 else '.'

        self.observer.schedule(self.event_handler, self.path, recursive=True)
        self.observer.start()
