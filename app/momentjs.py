from jinja2 import Markup

class momentjs(object):
    def __init__(self, timestamp):
        self.timestamp = timestamp

    def fromNow(self):
        return self.timestamp.strftime("%Y-%m-%d  %H:%M:%S")