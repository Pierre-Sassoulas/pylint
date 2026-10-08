"""Hi!"""
import pywintypes

try:
    raise pywintypes.error
except pywintypes.error:
    print('It works')
