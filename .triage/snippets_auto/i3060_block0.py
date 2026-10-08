"""Lorem ipsum"""

import pandas as pd


def demo():
    """Demo for the false positive"""
    with pd.ExcelWriter("demo.xlsx") as writer:
        print(writer)
