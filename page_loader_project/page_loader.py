import os
import requests
import re
from os.path import splitext

from bs4 import BeautifulSoup


def get_file_name(url: str):
    schema = url.find('://')
    url = url[schema + 3:]
    url = re.split(r'\W+', url)
    url = '-'.join(url) + '.html'
    return url


def get_files_path(url: str):
    html_file = get_file_name(url)
    path, ext = splitext(html_file)
    path_for_files = path + '_files'
    return path_for_files


def find_pics(file: str):
    with open(file) as file:
        soup = BeautifulSoup(file, 'html.parser')
        images = soup.find_all('img')
        if not images:
            return None
        return [img.get('src') for img in images
                if img.get('src').endswith('.png')
                or img.get('src').endswith('.jpg')]


def get_pic_name(url: str, src: str, directory: str):
    files_storage = get_files_path(url)
    path, ext = splitext(src)
    file_name = re.split(r'\W+', path[1:])
    if ext == '.png':
        file_name = '-'.join(file_name) + '.png'
    else:
        file_name = '-'.join(file_name) + '.jpg'
    return directory + '/' + files_storage + '/' + file_name


def get_new_src_in_html(url: str, src: str):
    files_storage = get_files_path(url)
    path, ext = splitext(src)
    file_name = re.split(r'\W+',
                         path[7:] if src.startswith('http:/') else path[8:])
    if ext == '.png':
        file_name = '-'.join(file_name) + '.png'
    else:
        file_name = '-'.join(file_name) + '.jpg'
    return files_storage + '/' + file_name


def save_pic(url: str, file, directory: str):
    images_in_file = find_pics(file)
    if url[-1] == '/':
        url = url[:len(url) - 1]
    if images_in_file:
        for image_src in images_in_file:
            img = requests.get(image_src)
            picture_storage = get_pic_name(url, image_src, directory)
            with open(picture_storage, 'wb') as img_storage:
                img_storage.write(img.content)
    return


def edit_html(url: str, file: str):
    opened_file = open(file)
    soup = BeautifulSoup(opened_file, 'html.parser')
    images = soup.find_all('img')
    for image in images:
        new_src = get_new_src_in_html(url, image.get('src'))
        image['src'] = new_src
    to_write = soup.prettify()
    opened_file.close()
    opened_file = open(file, 'w')
    opened_file.write(to_write)
    opened_file.close()


def download(url: str, directory=os.getcwd()):
    path = directory + '/' + get_file_name(url)
    html = requests.get(url).text
    os.mkdir(directory + '/' + get_files_path(url))
    with open(path, 'w') as output:
        output.write(html)
    save_pic(url, path, directory)
    edit_html(url, path)
    return path
