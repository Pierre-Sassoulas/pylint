import sys

if sys.platform == "linux":
    import os

    print(os.getgroups())
    print([group for group in os.getgroups()])
    print({group for group in os.getgroups()})
