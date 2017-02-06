

import sys
from transform import Transformer


def show_usage():
    print "main.py input.swf"

if __name__ == "__main__":
    print "Start runing"
    print sys.argv

    swfPath = ""

    if len(sys.argv) == 1:
        show_usage()
        # exit(0)
        swfPath = "test.swf"
    else:
        swfPath = sys.argv[1]

    trans = Transformer()

    trans.start(swfPath)

