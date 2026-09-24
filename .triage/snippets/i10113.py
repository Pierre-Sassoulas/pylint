import subprocess


def __func():
    comm = None
    p = subprocess.Popen("")
    try:
        comm = p.communicate(timeout=10)
    except subprocess.TimeoutExpired:
        pass
    stdout, _ = comm
    return stdout


def f():
    s = __func()
    pos = s.find(" ")
    if not pos == -1:
        pass
