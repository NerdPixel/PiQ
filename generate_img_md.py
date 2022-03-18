from os import walk
import re
from functools import cmp_to_key
import numpy as np


def write_link(file, text, url):
    file.write(f'[{text}]({url})')


def write_img(file, alt_text, img_path):
    file.write(f'![{alt_text}]({img_path} | width=100)')


def write_img_html(file, alt_text, img_path):
    file.write(f'<img src={img_path} width={200}>')

def sort_func(a, b):
    a_num = int(''.join(re.findall(r'\d+', a)))
    b_num = int(''.join(re.findall(r'\d+', b)))

    if a_num > b_num:
        return 1
    elif a_num == b_num:
        return 0
    elif a_num < b_num:
        return -1


if __name__ == '__main__':
    path = r"images_joh/original"

    img_files = []
    log_files = []
    categories = []

    for f_path, _, filename in walk(path):
        if 'landscape' in f_path or 'images_joh/original' == f_path:
            continue
        for file in filename:
            if file.endswith(".jpeg"):
                img_files.append(f'{f_path}/{file}')
            if file.endswith(".txt"):
                log_files.append(f'{f_path}/{file}')
        categories.append(f_path.replace('images_joh/original/', ''))

    img_files.sort(key=cmp_to_key(sort_func))
    img_files = list(np.array(img_files).reshape((10, 3)).T.flatten())
    print(img_files)

    log_lines = []
    print(log_files)
    for log in log_files:
        with open(log, 'r') as f:
            lines = f.readlines()
            lines = [line.replace("\\\n", "") for line in lines]
            log_lines.append(lines)
            f.close()

    log_lines = list(np.array(log_lines).flatten())
    print(log_lines)

    print(categories)
    with open('images.md', 'w') as f:
        f.write("# Images")
        f.write("\n")
        f.write("\n")
        for cat in categories:
            f.write(f"# {cat.capitalize()}")
            f.write("\n")
            f.write("\n")
            for img, link in zip(img_files, log_lines):
                if cat in img:
                    write_img_html(f, img.split("/")[-1], img)
                    f.write("\n")
                    f.write("\n")
                    write_link(f, "Link", link.split(" ")[-1])
                    f.write("\n")
                    f.write("\n")