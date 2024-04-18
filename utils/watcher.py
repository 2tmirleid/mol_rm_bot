import sys

from watchdog.events import LoggingEventHandler
from watchdog.observers import Observer


class Watcher:
    def __init__(self):
        ...

    def watch(self):
        path = sys.argv[1] if len(sys.argv) > 1 else '.'

        event_handler = LoggingEventHandler()
        observer = Observer()
        observer.schedule(event_handler, path, recursive=True)
        observer.start()
