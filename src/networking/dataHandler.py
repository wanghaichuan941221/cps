from threading import Timer

from control.controller import Controller


class DataHandler:

    def __init__(self, con: 'Controller'):
        self.con = con
        self.timer = Timer(0.5, self.con.stop_motors())
        self.top_view_data = None
        self.side_view_data = None

    def on_top_view_data(self, data):
        self.top_view_data = data
        if self.side_view_data is not None:
            self.flush()

    def on_side_view_data(self, data):
        self.side_view_data = data
        if self.top_view_data is not None:
            self.flush()

    def flush(self):
        self.timer.cancel()
        self.con.update_data(self.top_view_data, self.side_view_data)
        self.top_view_data = None
        self.side_view_data = None
        self.timer.start()
