#!/usr/bin/env python3
import sys
import inspect
import importlib

def patch_event(orig_func, new_func):
    def patch_func(*args, **kwargs):
        new_func(*args, **kwargs)
        return orig_func(*args, **kwargs)

    return patch_func

def main():

    qtcore = importlib.import_module('qtpy.QtCore')
    qtwidgets = importlib.import_module('qtpy.QtWidgets')

    widget_registry = {}

    def register_widget(*args, **kwargs):
        widget = args[0]
        frames = inspect.stack()
        for i, frame_info in enumerate(reversed(frames)):
            if frame_info.function == '__init__':
                widget_registry[widget] = frames[i-1]
                break

    def handle_mouse_click(*args, **kwargs):
        widget = args[0]
        frame_info = widget_registry[widget]
        info = "{}:{} {}".format(frame_info.filename,
                                 frame_info.lineno,
                                 frame_info.code_context)
        print(widget, info)

    qtwidgets.QWidget.__init__ = patch_event(qtwidgets.QWidget.__init__,
                                             register_widget)
    qtwidgets.QWidget.mousePressEvent = patch_event(qtwidgets.QWidget.mousePressEvent,
                                                    handle_mouse_click)

    sys.modules['qtpy.QtCore'] = qtcore
    sys.modules['qtpy.QtWidgets'] = qtwidgets

    from cubeviz.cubeviz import main as cubeviz_main
    cubeviz_main()


if __name__ == '__main__':
    main()
