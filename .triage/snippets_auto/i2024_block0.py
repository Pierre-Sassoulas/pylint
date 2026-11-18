>cat bug.py
"""Code runs without error"""
import tensorflow as tf
print(tf.Summary().value)
print("Done")

>python bug.py
[]
Done

>pylint bug.py
No config file found, using default configuration
************* Module bug
E:  3, 6: Instance of 'Summary' has no 'value' member; maybe 'Value'? (no-member)

--------------------------------------------------------------------
Your code has been rated at -6.67/10 (previous run: -6.67/10, +0.00)

