from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import sys
import glob
import os
import argparse
import collections


if sys.version_info[0] == 3:
    from os import walk
else:
    from os.path import walk


work_dir = '/home/pi/Temp/bib_test/'
gift = '_1' # suffix for double file


def main(work_dir, gift):
    for root, dirs, files in os.walk(work_dir):
        for _dir in dirs:
            files_path = sorted(glob.glob(os.path.join(root, _dir)+'/*'))
            files_path = [f for f in files_path if os.path.isfile(f)]

            if files_path:
                up_basenames = [os.path.basename(f).upper() for f in files_path]
                for i, file_path in enumerate(files_path):
                    move = False
                    ori_file_path = file_path
                    head, tail = os.path.split(file_path)

                    if ' ' in tail:
                        new_tail = tail.replace(' ', '_')
                        new_path = os.path.join(root, _dir, new_tail)
                        files_path[i] = new_path
                        print('SPACE "{}" -> {}'.format(file_path, new_tail))
                        move = True
                        file_path = new_path
                        up_basenames[i] = new_tail.upper()

                    head, tail = os.path.split(file_path)

                    while collections.Counter(up_basenames)[tail.upper()] > 1:
                        if '.' in tail:
                            new_tail = tail.replace('.', gift+'.')
                        else:
                            new_tail = tail + gift

                        up_basenames[i] = new_tail.upper()
                        new_path = os.path.join(root, _dir, new_tail)
                        files_path[i] = new_path
                        print('Double "{}" -> {}'.format(file_path, new_tail))
                        move = True
                        tail = new_tail
                        file_path = new_path

                    if move:
                        os.rename(ori_file_path, file_path)


if __name__ == "__main__":
    main(work_dir, gift)
