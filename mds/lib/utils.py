import os

import psutil


def kill_other_drivers():
    """It searches if there are any other drivers running, it kills them to start our process if so"""
    cmd = [
        "ps",
        "-U",
        os.environ.get("USER"),
        "-f",
        "|",
        "grep",
        "python",
        "|",
        "grep",
        os.path.basename(__file__),
        "|",
        "grep",
        "-v",
        str(os.getpid()),
        "|",
        "grep",
        "-v",
        "grep",
        "|",
        "grep",
        "-v",
        "mp_dwld_driver_log_",
        "|",
        "awk",
        "'{{ print $2 }}'",
    ]
    print(cmd)
    seperator = " "
    parent_pid = os.popen(seperator.join(cmd)).read()
    print(parent_pid)
    if parent_pid:
        parent_proc = int(parent_pid)
        parent = psutil.Process(parent_proc)
        for child in parent.children(recursive=True):
            child.kill()
        parent.kill()


def suicide_if_needed():
    """
    It searches if there are any other drivers running, returns a non empty array (of other pids) if so.
    """
    cmd = []
    cmd += [
        "ps",
        "-U",
        os.environ.get("USER"),
        "-f",
        "|",
        "grep",
        "python",
        "|",
        "grep",
        os.path.basename(__file__),
        "|",
        "grep",
        "-v",
        str(os.getpid()),
        "|",
        "grep",
        "-v",
        "grep",
        "|",
        "grep",
        "-v",
        "mp_dwld_driver_log_",
        "|",
        "awk",
        "'{{ print $2 }}'",
    ]
    print(cmd)
    seperator = " "
    parent_pid = os.popen(seperator.join(cmd)).read()
    print(parent_pid)
    return parent_pid


def time_to_seconds(time_string):
    hours, minutes = map(int, time_string.split(":"))
    return hours * 3600 + minutes * 60
