import subprocess

command = ["myprogram"]
run_kwargs = {"check": True}
subprocess.run(command, **run_kwargs)  # raise a subprocess-run-check
