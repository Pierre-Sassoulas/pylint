"https://github.com/pylint-dev/pylint/issues/"
import matplotlib.pyplot as plt
def figrow(figsize, ncols):
    "Return figure and axes for a row with ncol columns."
    if not isinstance(figsize[0], int):
        return figsize
    return plt.subplots(figsize=(ncols*figsize[0], figsize[1]),nrows=1,ncols=ncols)
fig, axes = figrow(figsize=(4,7), ncols=3)
axes[0].plot([1,2,3],[4,5,6])
fig.tight_layout()
