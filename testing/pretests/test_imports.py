import subprocess
import sys


def _ask_permsision(library_name):
    '''
    Checks whether the import library is installed or not, and if not installed,
    ask for persmission to install or not using Y/N(y/n). If given other input,
    ask again

    Arguments:
        library_name : The library Name as string
    '''
    perm = input(f'{library_name} is not Installed, Would you like to install Y/N? ')
    if perm in ('y', 'Y'):
        subprocess.check_call([sys.executable, "-m", "pip",
                           "install", library_name])
    elif perm in ('n', 'N'):
        print(f'{library_name} NOT installed, this may cause issues!')
    else:
        print('Invalid Input!')
        _ask_permsision(library_name)


try:
    import cv2 as cv
except ImportError:
    _ask_permsision('opencv-python')

try:
    from PIL import ImageFont, Image, ImageDraw
except ImportError:
    _ask_permsision('Pillow')

try:
    import numpy as np
except ImportError:
    _ask_permsision('numpy')

try:
    import pytest
except ImportError:
    ask_permsision('pytest')
