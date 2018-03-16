#!/usr/bin/env python3
import sys
import importlib

def patch_event(orig_func):
    def patch_func(*args, **kwargs):
        print(args, kwargs)
        return orig_func(*args, **kwargs)

    return patch_func

def main():

    qtcore = importlib.import_module('qtpy.QtCore')
    qtcore.QObject.__init__ = patch_event(qtcore.QObject.__init__)

    sys.modules['qtpy.QtCore'] = qtcore

    from cubeviz.cubeviz import main as cubeviz_main
    cubeviz_main()


if __name__ == '__main__':
    main()
