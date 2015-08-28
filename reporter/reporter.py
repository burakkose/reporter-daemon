import argparse
import logging
import os
import shutil
import tempfile
import time

from generator import ReportGenarator
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

__author__ = "Burak KÖSE"
__email__ = "burakks41@gmail.com"

# Defaults
LOG_FILE = os.path.join(tempfile.gettempdir(), "reporter.log")
LOG_LEVEL = logging.DEBUG

logging.basicConfig(filename=LOG_FILE, level=LOG_LEVEL,
                    format="%(asctime)s - %(levelname)s : %(message)s",
                    datefmt="%m/%d/%Y %I:%M:%S %p")

parser = argparse.ArgumentParser(description='PDF Generator')


class Tracker(PatternMatchingEventHandler):
    patterns = ["*.xml"]

    def __init__(self, inputf, outputf):
        PatternMatchingEventHandler.__init__(self)

        self.output = outputf
        self.finished = os.path.join(inputf, 'finished')

        if not os.path.exists(self.output):
            os.makedirs(self.output)
        if not os.path.exists(self.finished):
            os.makedirs(self.finished)

    def process(self, event):
        """
        event.event_type
            'created'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        ReportGenarator(event.src_path, self.output).create_pdf()
        shutil.move(event.src_path, self.finished)

    def on_created(self, event):
        self.process(event)


def run_as_a_daemon(inputf, outputf):
    observer = Observer()
    observer.schedule(Tracker(inputf, outputf), path=inputf)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


def main():
    """Main function"""
    logging.info("[>                Reporter is starting                ] 0%")
    parser.add_argument("input", help="The path of input file or folder")
    parser.add_argument("output", help="The path of output file or folder")
    parser.add_argument("-f", "--folder", action='store_true',
                        help="Track folder and process all file continuously")
    args = parser.parse_args()

    if args.folder:
        run_as_a_daemon(args.input, args.output)
    else:
        ReportGenarator(args.input, args.output).create_pdf()

    logging.info("[====================================================] 100%")

if __name__ == "__main__":
    main()
