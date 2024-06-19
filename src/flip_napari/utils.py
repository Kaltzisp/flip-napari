import time
from napari.utils import notifications


class Timer:
    def __init__(self, name):
        self.start_time = time.time()
        self.name = name

    def print_duration(self):
        start_time = int(self.start_time)
        end_time = int(time.time())
        minutes = (end_time - start_time) // 60
        seconds = (end_time - start_time) % 60
        elapsed_time = f"Completed {self.name} in {minutes:02}mins {seconds}secs"
        notifications.show_info(elapsed_time)


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
