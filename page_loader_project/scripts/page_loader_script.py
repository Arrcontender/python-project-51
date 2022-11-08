#!/usr/bin/env python3

import argparse
import os

from page_loader_project.page_loader import download


def main():
    parser = argparse.ArgumentParser(
        description="Utility downloads page and returns html file's path")
    parser.add_argument('url_to_page', type=str)
    parser.add_argument('--output', default=os.getcwd())
    args = parser.parse_args()
    result = download(args.url_to_page, args.output)
    print(result)


if __name__ == '__main__':
    main()
