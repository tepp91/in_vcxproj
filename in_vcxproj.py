import os
import argparse
import re
import xml.etree.ElementTree as ET
from pathlib import Path


# ----------------------------------------------------------------------
def make_set_in_vcxproj(proj_path):
    tree = ET.parse(proj_path)
    root = tree.getroot()

    ns = re.match('\{(.*)\}', root.tag).group(1)

    file_set = set()

    for elem in root.findall('.//ns:ItemGroup/ns:ClInclude', {'ns': ns}):
        file_set.add(elem.attrib['Include'])

    for elem in root.findall('.//ns:ItemGroup/ns:None', {'ns': ns}):
        file_set.add(elem.attrib['Include'])

    for elem in root.findall('.//ns:ItemGroup/ns:ClCompile', {'ns': ns}):
        file_set.add(elem.attrib['Include'])

    proj_dir = os.path.dirname(proj_path)
    file_set = {os.path.normpath(os.path.join(proj_dir, x)) for x in file_set}

    return file_set

# ----------------------------------------------------------------------
def make_set_in_dir(dir_path):
    file_set = set()
    ext_list = ['.cpp', '.h', '.inl', '.c', '.hpp']

    p = Path(dir_path)
    for filepath in [x for x in p.glob('**/*') if x.suffix in ext_list]:
        file_set.add(str(filepath))

    return {os.path.normpath(x) for x in file_set}


# ----------------------------------------------------------------------
def check_not_exist(file_set):
    not_exist_set = set()
    for filepath in file_set:
        if not os.path.exists(filepath):
            print(filepath)
            not_exist_set.add(filepath)

    return not_exist_set


# ----------------------------------------------------------------------
def output(file_set):
    for filepath in file_set:
        print(filepath)


# ----------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('proj_path')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-ne', action='store_true')
    group.add_argument('-dir');

    args = parser.parse_args()

    if not os.path.isfile(args.proj_path):
        print('The specified path does not exist.')
        return

    vcxproj_set = make_set_in_vcxproj(args.proj_path)
    if args.ne:
        output(check_not_exist(vcxproj_set))
    elif args.dir is not None:
        if os.path.isdir(args.dir):
            dir_set = make_set_in_dir(args.dir)
            output(dir_set - vcxproj_set)
        else:
            print('The specified path does not exist.')
    else:
        output(vcxproj_set)


# ----------------------------------------------------------------------
if __name__ == '__main__':
    main()
