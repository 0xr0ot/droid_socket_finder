import os
import sys
import re
from subprocess import Popen, PIPE
from blessings import Terminal
from datetime import datetime

# Globals
t = Terminal()
root = os.path.dirname(os.path.realpath(__file__))
adb = "".join([root, "/bin/adb"])

def cmd(args):
    """
    Execute adb commands
    """
    try:
        p = Popen(["{} shell {}".format(adb, args)], shell=True, stdout=PIPE, stderr=PIPE)
        out,err = p.communicate()
        if out:
            return out
    except Exception as e:
        raise e
    return

def process_uid(protocol, entry):
    """
    Extract UID from /proc/net entry
    """
    if protocol == "tcp" or protocol == "tcp6":
        uid = entry.split()[-10]
    else:
        uid = entry.split()[-6]
    uid = int(uid)
    if uid > 10000:
        return "".join(["u0_a", str(uid - 10000)])
    else:
        return -1


def to_hex(p):
    """
    Convert port number to hex representation
    """
    h = str(hex(int(p)))
    return h.strip('0x').upper()

def finder():
    """
    Map applications to listening sockets
    """
    # Locals
    apps = list()
    stripped = list()
    pattern = re.compile("^Proto")
    # Get netstat result
    netstat = cmd("netstat | grep -Ei 'listen|udp*'")
    print(t.yellow("[{}] Running search ...".format(datetime.now())))
    if netstat:
        for line in netstat.split("\r\n"):
            if line and pattern.match(line) == None:
                socket = line.split()
                protocol = socket[0]
                port = socket[3].split(':')[-1]
                if protocol and port:
                    app = cmd("grep {} /proc/net/{}".format(to_hex(port), protocol))
                    uid = process_uid(protocol, app)
                    if uid == -1:
                        continue
                    application_list = cmd("ps | grep '{}' ".format(uid)).split()
                    app = application_list[8]
                    apps.append(app)
                    stripped.append(line)
    # Build apps and lines
    iterated_apps = iter(apps)
    iterated_lines = iter(stripped)

    try:
        while True:
            print(t.yellow("-" * 150))
            for i in range(0, len(apps)):
                print(t.yellow("[{}] {}\t\t{}".format(i, iterated_apps.next(), iterated_lines.next())))
            #print(t.magenta("{}\t{}".format(iterated_apps.next(), iterated_lines.next().split())))
    except StopIteration:
        pass



if __name__ == "__main__":
    try:
        finder()
    except KeyboardInterrupt:
        sys.exit(0)
