import time
from napari.utils import notifications


class Timer:
    def __init__(self, message):
        self.spawn_time = time.time()
        self.restart(message)

    def restart(self, message):
        self.start_time = time.time()
        notifications.show_info(message + "...")

    @staticmethod
    def get_elapsed(start_time):
        start_time = int(start_time)
        end_time = int(time.time())
        minutes = (end_time - start_time) // 60
        seconds = (end_time - start_time) % 60
        return f"{minutes:02}mins {seconds}secs"

    def print_duration(self):
        message = Timer.get_elapsed(self.start_time)
        notifications.show_info("Time taken: " + message)

    def end(self):
        message = Timer.get_elapsed(self.spawn_time)
        notifications.show_info("Completed in: " + message)


class Widgets:

    @classmethod
    def FileWidget(cls, label, tooltip):
        return {"label": label, "widget_type": "FileEdit", "tooltip": tooltip}

    @classmethod
    def TextWidget(cls, label, tooltip):
        return {"label": label, "widget_type": "LineEdit", "tooltip": tooltip}

    @classmethod
    def FloatWidget(cls, label, tooltip, min, max, step, value):
        return {"label": label, "widget_type": "FloatSlider", "tooltip": tooltip, "min": min, "max": max, "step": step, "value": value}
