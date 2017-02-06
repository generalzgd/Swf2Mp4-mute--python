#！ /usr/bin/evn python
# encoding: utf-8

'''
@version: 1.0.0
@author: zgd: general_zgd
@license: LGPL v3
@contact: general_zgd@163.com
@site: github.com/generalzgd
@software: PyCharm Community Edition
@file: main.py
@time: 17-2-6 下午4:16
'''

import sys
from transform import Transformer


def show_usage():
    print "Usage:: main.py /input.swf"

if __name__ == "__main__":
    print "Start runing"
    print sys.argv

    swfPath = ""

    if len(sys.argv) == 1:
        show_usage()
        exit(0)
        # swfPath = "/home/zgd/PycharmProjects/Swf2MuteMp4-python/test.swf"
        # swfPath = "test.swf"
    else:
        swfPath = sys.argv[1]

    trans = Transformer()

    trans.start(swfPath)

    print "Swf tansfor to Mp4 successed!!!!"

