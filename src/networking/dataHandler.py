from threading import Timer, RLock

from control.controller import Controller


class DataHandler:

    def __init__(self, con: 'Controller'):
        self.con = con
        self.top_view_data = None
        self.left_view_data = None
        self.right_view_data = None

    def on_top_view_data(self, data):
        self.top_view_data = data
        if self.all_data_present():
            self.flush()

    def on_left_view_data(self, data):
        self.left_view_data = data
        if self.all_data_present():
            self.flush()

    def on_right_view_data(self, data):
        self.right_view_data = data
        if self.all_data_present():
            self.flush()

    def flush(self):
        self.con.update_data(self.top_view_data, self.left_view_data, self.right_view_data)

        self.top_view_data = None
        self.left_view_data = None
        self.right_view_data = None

    def all_data_present(self):
        return (self.top_view_data is not None and
                self.left_view_data is not None and
                self.right_view_data is not None)


