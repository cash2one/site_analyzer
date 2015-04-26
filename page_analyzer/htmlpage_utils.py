#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

html_dir = 'html_pages'


def load_html_page(file_name):

    root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))  # the project root directory
    full_file_name = os.path.join(root_dir, html_dir, file_name)
    #print full_file_name
    with open(full_file_name) as f:
        text = f.read()

    return text