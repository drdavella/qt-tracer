#!/usr/bin/env python3
import sys
import importlib

def patch_event(orig_func, new_func):
    def patch_func(*args, **kwargs):
        new_func(*args, **kwargs)
        return orig_func(*args, **kwargs)

    return patch_func

def main():

    qtcore = importlib.import_module('qtpy.QtCore')

    def handle_mouse_click(*args, **kwargs):
        self, obj, event = args[:3]
        if event.type() == qtcore.QEvent.MouseButtonPress:
            print(self, obj, event)

    qtcore.QObject.eventFilter = patch_event(qtcore.QObject.eventFilter, handle_mouse_click)

    sys.modules['qtpy.QtCore'] = qtcore

    from cubeviz.cubeviz import main as cubeviz_main
    cubeviz_main()


if __name__ == '__main__':
    main()
