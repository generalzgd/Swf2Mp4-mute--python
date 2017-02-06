#！ /usr/bin/evn python
# encoding: utf-8

'''
@version: 1.0.0
@author: zgd: general_zgd
@license: LGPL v3
@contact: general_zgd@163.com
@site: github.com/generalzgd
@software: PyCharm Community Edition
@file: transform.py
@time: 17-2-6 下午4:16
'''

__author__ = "general_zgd"
__version__ = "1.0.0"

import swffile
import os
import subprocess
import shutil


class Transformer:
    def __init__(self):
        self.TEMP_profix = "TMP_"
        self.AUDIO_suffix = ".TMP.wav"
        self.TEMP_IMG_FORMAT = "TMP_%f.png"
        pass

    def __clean_dir(self, dirc):
        if os.path.exists(dirc):
            if os.path.isdir(dirc):
                paths = os.listdir(dirc)
                for path in paths:
                    filePath = os.path.join(dirc, path)
                    if os.path.isfile(filePath):
                        try:
                            os.remove(filePath)
                        except os.error:
                            print "remove file {0} fail!".format(filePath)
                    elif os.path.isdir(filePath):
                        shutil.rmtree(filePath, True)

    """"""
    def start(self, swfPath):
        print swfPath
        # print os.path.relpath(swfPath)
        # print os.path.isabs(swfPath)
        if os.path.exists(swfPath) == False or os.path.isdir(swfPath):
            print "Input swf file do not exist"
            exit()

        # parse file infomation
        self.__parse_swf_file(swfPath)

        # extracting audio
        # self.audio_file = os.path.join(os.path.dirname(swfPath), os.path.basename(swfPath) + self.AUDIO_suffix)
        # self.__extract_audio(swfPath, self.audio_file)

        # start save frame image
        # create temp directory
        swfName, extension = os.path.splitext(os.path.basename(swfPath))
        self.temp_dir = os.path.join(os.path.dirname(swfPath), self.TEMP_profix + swfName)
        self.temp_frame_img_format = os.path.join(self.temp_dir, self.TEMP_IMG_FORMAT)

        if os.path.exists(self.temp_dir):
            if os.path.isdir(self.temp_dir):
                shutil.rmtree(self.temp_dir, True)
            else:
                os.remove(self.temp_dir)
        os.mkdir(self.temp_dir)
        self.__save_frame_img(swfPath, self.temp_frame_img_format)

        self.mp4_path = os.path.join(os.path.dirname(swfPath), swfName + ".mp4")
        if os.path.exists(self.mp4_path):
            if os.path.isdir(self.mp4_path):
                shutil.rmtree(self.mp4_path, True)
            else:
                os.remove(self.mp4_path)
        self.__merge_mp4(self.temp_frame_img_format, self.mp4_path)

        # remove temp directory
        try:
            shutil.rmtree(self.temp_dir, True)
        except:
            pass

    def __extract_audio(self, swfPath, audioPath):
        audio_result = subprocess.Popen(['gnash', '--once', '-A', audioPath, '-r', '2', swfPath], shell=True)
        audio_result.wait()
        if audio_result.returncode != 0:
            print "Someting wrong when extract audio"
            exit()

    def __save_frame_img(self, swfPath, frameFormat):
        # gnash
        # --once --screenshot 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24
        # --screenshot-file TMP_test/TMP_%f.png
        # test.swf
        frame_list = [str(id) for id in range(1, self.frame_count+1)]
        frame_str = ",".join(frame_list)
        args = ['gnash', '--once', '--screenshot', frame_str, '--screenshot-file', frameFormat, swfPath]
        # args = ['gnash']
        screen_result = subprocess.Popen(args=args)
        screen_result.wait()
        if screen_result.returncode != 0:
            print "Something wrong when extract frame image"
            exit()

    def __merge_mp4(self, frameFormat, mp4Path):
        # ffmpeg -f image2 -i TMP_test/TMP_%d.png -vcodec libx264 -threads 0 -r 24 -g 50 -b 500k - y test.mp4
        args = ['ffmpeg', '-f', 'image2', '-i', frameFormat.replace("%f", "%d"), '-vcodec', 'libx264', '-threads', '0',
                '-r', str(int(self.frame_rate)), '-g', '50', '-b', '500k', '-y', mp4Path]
        print args
        ffmpeg_result = subprocess.Popen(args=args)
        ffmpeg_result.wait()
        if ffmpeg_result.returncode != 0:
            print "Something wrong when merge Mp4 file!"
            exit()

    def __parse_swf_file(self, swfPath):
        f = swffile.Flash(swfPath)
        self.output_width = f.header.MovieWidth
        self.output_height = f.header.MovieHeight
        self.frame_rate = f.header.FrameRate
        self.frame_count = f.header.FrameCount
        self.bgColor = f.SetBackgroundColor.BackgroundColor

        self.__print_swf_info(f)

    def __print_swf_info(self, f):
        print "\nHeader:"
        print "     Version: %d" % f.header.Version
        print "  FileLength: %s" % f.header.FileLength
        print "       Twips: %d x %d" % (
        f.header.FrameSize.Xmax - f.header.FrameSize.Xmin, f.header.FrameSize.Ymax - f.header.FrameSize.Ymin)
        print "      Pixels: %d x %d" % (f.header.MovieWidth, f.header.MovieHeight)
        print "   FrameRate: %d" % f.header.FrameRate
        print "  FrameCount: %d" % f.header.FrameCount

        print "\nFlags: %08x" % f.Flags.Value
        print "  UseDirectBlit: ", f.Flags.UseDirectBlit
        print "         UseGPU: ", f.Flags.UseGPU
        print "    HasMetadata: ", f.Flags.HasMetadata
        print "  ActionScript3: ", f.Flags.ActionScript3
        print "     UseNetwork: ", f.Flags.UseNetwork