#!/usr/bin/env python3

from os import walk, path
import hashlib
import argparse

parser = argparse.ArgumentParser(description="The utility takes the path to "
                                             "the directory and sha256 hash "
                                             "as an arguments. It goes through"
                                             " all the files inside the "
                                             "directory and displays in stdout"
                                             " the absolute path to the files"
                                             " whose hash is specified as an "
                                             "argument.")
parser.add_argument('inp_path', type=str, help='Path to directory')
parser.add_argument('inp_hash', type=str, help='Hash of the file(s)')
args = parser.parse_args()

inp_path = args.inp_path
inp_hash = args.inp_hash


def get_hash(filename):
    """Get hash of the given file"""
    with open(filename, "rb") as f:
        raw_string = f.read()
        readable_hash = hashlib.sha256(raw_string).hexdigest()
        return readable_hash


def return_path_of_specified_hash(inp_path, sha256):
    """Returns absolute path of the file with hash equal to the
    specified sha256 hash"""
    tree = walk(inp_path)
    paths = []
    for root, dirs, files in tree:
        for file in files:
            cwd = path.abspath(root)
            root_file = cwd + '/' + file
            processed_hash = get_hash(root_file)
            if processed_hash == inp_hash:
                paths.append(root_file)
    return paths


ans = return_path_of_specified_hash(inp_path, inp_hash)

print()
if ans:
    print('The following files were found: ')
    print(*ans, sep='\n')
else:
    print('There is no files with such hash')
