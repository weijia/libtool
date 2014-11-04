import os
import sys


def include_file_folder(file_path):
    include(os.path.dirname(file_path))


def include(folder):
    folder = os.path.abspath(folder)
    if not (folder in sys.path):
        sys.path.insert(0, folder)


def append(folder):
    folder = os.path.abspath(folder)
    if not (folder in sys.path):
        sys.path.append(folder)


def include_in_folder(folder, sub_folder_name):
    include(os.path.join(folder, sub_folder_name))