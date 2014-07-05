#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import inspect
import logging
from filetools import main_is_frozen, get_sibling_folder

log = logging.getLogger(__name__)


def find_root_path(file_path, root_folder_name):
    in_file_path = file_path
    folder_name = None
    while folder_name != root_folder_name:
        folder_name = os.path.basename(file_path)
        #log.error("find_root_path:"+folder_name)
        last_file_path = file_path
        file_path = os.path.dirname(file_path)
        if last_file_path == file_path:
            print "find root path failed, last_file_path: %s, file_path: %s, folder_name: %s, root_folder_name: %s" % (last_file_path,
                                file_path, folder_name, root_folder_name)
            raise "No root path found"
    found_path = os.path.join(file_path, root_folder_name)
    #log.error("returning:"+found_path)
    return os.path.abspath(found_path)


def include_root_path(file_path, root_folder_name):
    include(find_root_path(file_path, root_folder_name))


def include_sub_folder_in_root_path(file_path, root_folder_name, folder_name):
    root_folder_path = find_root_path(file_path, root_folder_name)
    include_in_folder(root_folder_path, folder_name)


def find_root_path_from_pkg(package_info):
    return find_root_path(package_info.file_path, package_info.package_root_name)


def include_sub_folder(package_info, folder_name):
    root_folder_path = find_root_path(package_info)
    include_in_folder(root_folder_path, folder_name)


def include_folders(lib__full_path_list):
    for i in lib__full_path_list:
        include(i)


def get_file_folder(file_path):
    folder = os.path.abspath(os.path.dirname(file_path))
    return folder


def include_file_sibling_folder(file_path, sub_folder_name):
    if (file_path[-1] == "/") or (file_path[-1] == "\\"):
        file_path = file_path[0:-1]
    folder = get_file_folder(file_path)
    include_in_folder(folder, sub_folder_name)


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


def exclude(folder):
    folder = os.path.abspath(folder)
    if folder in sys.path:
        sys.path.remove(folder)


def get_grand_parent(folder_path):
    return get_parent_folder_for_folder(get_parent_folder_for_folder(folder_path))


def get_parent_of_folder_containing_file(file_path):
    #print "parent:"+os.path.abspath(os.path.join(os.path.dirname(file_path),".."))
    return os.path.abspath(os.path.join(os.path.dirname(file_path),".."))


def get_parent_folder_for_folder(folder_path):
    return os.path.abspath(os.path.join(folder_path,".."))


def include_all_direct_subfolders(folder_path):
    for i in os.listdir(folder_path):
        full_path = os.path.abspath(os.path.join(folder_path, i))
        if os.path.isdir(full_path):
            append(full_path)


def include_all_direct_sub_folders_in_sibling(file_path, folder_name):
    include_all_direct_subfolders(get_sibling_folder(file_path, folder_name))


def is_package_root(full_path):
    return os.path.isdir(full_path) or ".zip" in full_path


def include_all_ext_packages(folder_path, lib_checker=is_package_root):
    for i in os.listdir(folder_path):
        full_path = os.path.abspath(os.path.join(folder_path, i))
        if lib_checker(full_path):
            append(full_path)


def include_all(file_path, folder_name):
    include_all_ext_packages(get_sibling_folder(file_path, folder_name))


def get_current_path():
    frame = inspect.getouterframes(inspect.currentframe())
    caller_frame = frame[1]
    dirpath = os.path.abspath(os.path.dirname(caller_frame[1]))
    return dirpath


def find_root(root_name, caller_level=1):
    frame = inspect.getouterframes(inspect.currentframe())
    caller_frame = frame[caller_level]
    caller_file = os.path.abspath(caller_frame[1])
    return find_root_path(caller_file, root_name)


def find_root_even_frozen(root_name):
    if main_is_frozen():
        #log.error("frozen, "+find_root_path(sys.executable, root_name))
        return find_root_path(sys.executable, root_name)
    else:
        #log.error(dir(sys))
        return find_root(root_name, 2)


def include_sub_folder_in_root_path_ex( root_folder_name, folder_name):
    frame = inspect.getouterframes(inspect.currentframe())
    caller_frame = frame[1]
    caller_file = caller_frame[1]
    root_folder_path = find_root_path(caller_file, root_folder_name)
    include_in_folder(root_folder_path, folder_name)


def get_parent_frame():
    frame = inspect.getouterframes(inspect.currentframe())
    caller_frame = frame[2]
    caller_file = caller_frame[1]
    return caller_file


def include_file_sibling_folder_ex(sub_folder_name):
    caller_file = get_parent_frame()
    if (caller_file[-1] == "/") or (caller_file[-1] == "\\"):
        caller_file = caller_file[0:-1]
    folder = get_file_folder(caller_file)
    include_in_folder(folder, sub_folder_name)
    
    
def include_sibling_file(file_path, filename):
    if (file_path[-1] == "/") or (file_path[-1] == "\\"):
        file_path = file_path[0:-1]
    folder = get_file_folder(file_path)
    include(os.path.join(folder, filename))


def add_path_to_python_path_env(full_path):
    full_path = full_path.replace("\\", "/")
    original = os.environ.get("PYTHONPATH", "")
    separator = ";"  # Only for windows, TODO: need to add cross platform support
    original_paths = original.split(separator)
    for original_path in original_paths:
        formatted_original = original_path.replace("\\", "/")
        if full_path == formatted_original:
            return
    original_paths.append(full_path)
    os.environ["PYTHONPATH"] = separator.join(original_paths)