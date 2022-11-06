import os
import requests
import re


def get_file_name(url: str):
    schema = url.find('://')
    url = url[schema + 3:]
    url = re.split(r'\W+', url)
    url = '-'.join(url) + '.html'
    return url


def download(url, directory=os.getcwd()):
    path = directory + '/' + get_file_name(url)
    html = requests.get(url).text
    with open(path, 'w') as output:
        output.write(html)
    return path
