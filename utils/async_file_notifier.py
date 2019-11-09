import pyinotify
import asyncio
import argparse
import os.path


class AsyncioNotifier(pyinotify.Notifier):
    """

    Notifier subclass that plugs into the asyncio event loop.
    From https://stackoverflow.com/questions/26414052/watch-for-a-file-with-asyncio
    Will only work on linux systems as it uses an inotify wrapper

    """
    def __init__(self, watch_manager, loop, callback=None,
                 default_proc_fun=None, read_freq=0, threshold=0, timeout=None):
        self.loop = loop
        self.handle_read_callback = callback
        pyinotify.Notifier.__init__(self, watch_manager, default_proc_fun, read_freq,
                                    threshold, timeout)
        loop.add_reader(self._fd, self.handle_read)

    def handle_read(self, *args, **kwargs):
        self.read_events()
        self.process_events()
        if self.handle_read_callback is not None:
            self.handle_read_callback(self)


class EventHandler(pyinotify.ProcessEvent):
    def my_init(self, file=None, loop=None):
        if not file:
            raise ValueError("file keyword argument must be provided")
        self.loop = loop if loop else asyncio.get_event_loop()
        self.filename = file

    def process_IN_CREATE(self, event):
        print("Creating:", event.pathname)
        if os.path.basename(event.pathname) == self.filename:
            print("Found it!")
            self.loop.stop()


def make_cli_parser():
    cli_parser = argparse.ArgumentParser(description=__doc__)
    cli_parser.add_argument('file_path')
    return cli_parser


def main(argv=None):
    cli_parser = make_cli_parser()
    args = cli_parser.parse_args(argv)
    loop = asyncio.get_event_loop()

    # set up pyinotify stuff
    wm = pyinotify.WatchManager()
    mask = pyinotify.IN_CREATE  # watched events
    dir_, filename = os.path.split(args.file_path)
    if not dir_:
        dir_ = "."
    wm.add_watch(dir_, mask)
    handler = EventHandler(file=filename, loop=loop)
    notifier = pyinotify.AsyncioNotifier(wm, loop, default_proc_fun=handler)

    loop.run_forever()

if __name__ == '__main__':
    main()