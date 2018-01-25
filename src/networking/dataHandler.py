from threading import Timer, RLock

from control.controller import Controller


class DataHandler:

    def __init__(self, con: 'Controller'):
        self.con = con
        self.timer = Timer(0.1, self.kill_switch)
        self.top_view_data = None
        self.side_view_data = None
        self.lock = RLock()

    def on_top_view_data(self, data):
        self.lock.acquire()

        self.top_view_data = data
        if self.side_view_data is not None:
            self.flush()

        self.lock.release()

    def on_side_view_data(self, data):
        self.lock.acquire()

        self.side_view_data = data
        if self.top_view_data is not None:
            self.flush()

        self.lock.release()

    def flush(self):
        self.timer.cancel()
        self.con.update_data(self.top_view_data, self.side_view_data)
        # self.con.update_data(self.top_view_data, [0,0,0,0,0,0,0,0,0,0])
        self.top_view_data = None
        self.side_view_data = None
        self.timer = Timer(0.5, self.con.stop_motors)
        self.timer.start()

    def kill_switch(self):
        self.con.stop_motors()
        print('HIT KILL SWITCH')
