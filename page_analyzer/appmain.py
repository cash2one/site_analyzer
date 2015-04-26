#!/usr/bin/python
# -*- coding: utf-8 -*-
# from django.contrib.auth import get_backends

from lxml import html
from lxml import etree
import re
import os
import urllib2
import socket
import errno
import httplib
from cookielib import LWPCookieJar
from urllib import quote_plus
from urllib2 import Request, urlopen
from urlparse import urlparse, parse_qs
from rank_provider import GooglePageRank


# Cookie jar. Stored at the user's home folder.
home_folder = os.getenv('HOME')
if not home_folder:
    home_folder = os.getenv('USERHOME')
    if not home_folder:
        home_folder = '.'  # Use the current folder on error.
cookie_jar = LWPCookieJar(os.path.join(home_folder, '.google-cookie'))
try:
    cookie_jar.load()
except Exception:
    pass





exclude_words_lst = ['a', 'the', 'at', 'of', 'and', 'or', 'on', 'to', 'he', 'she', 'it',]

def analyze_page(html_page_txt):
    """

    :param html_page_txt: string which contains html page
    :return: dictionary of page properties
        {Title,
    """
    pass


def extract_page_features(html_tree):
    """

    :param html_tree:
    :rtype: dictionary
    :return: extracted page features
        Title: string or None
        Description: string or None
        Headings: list of tags
        Images: list of tags
        Text: all text extracted from page or None
        In-Page Links: list of link tags
        Robots.txt: tag or None
        XML Sitemap: tag or None
        Flash: list of flash tags
        Frames: list of frame tags
    """
    page_features = {}
    return page_features


def extract_title(html_tree):
    e = html_tree.find('head').find('title')
    if e is not None:
        return e.text
    else:
        return None


def extract_description(html_tree):
    """
    <meta name="description" content="Free Web tutorials">
    :param html_tree:
    :return:
    """

    head = html_tree.find('head')
    for meta in head.iter('meta'):
        if 'name'in meta.attrib and meta.attrib['name'] == 'description':
            return meta.attrib['content']
    else:
        return None


def extract_heading(html_tree):
    """
    <h1>..<h6>
    :param html_tree:
    :return:
    """

    body = html_tree.find('body')
    output = []
    for e in body.iter('h1', 'h2', 'h3', 'h4', 'h5'):
        if e.text:
            l = [e.text]
        else:
            l = []
        extract_text(e, l)
        l2 = [i.strip() for i in l]
        output.append((e.tag, l2))
        # print l
        # print e.xpath('.//text()')
    return output

    # for e in body.iter():
    #     print e.tag


def traverse_tree(html_tree, elem_lst):
    for e in html_tree:
        if e.tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            txt_lst = []
            if e.text is not None:
                txt_lst += [(e.text).strip()]
            if e.tail is not None and len((e.tail).strip()) != 0:
                txt_lst += [(e.tail).strip()]
            if len(e) != 0:
                extract_text(e, txt_lst)
            elem_lst += [(e.tag, txt_lst)]
        elif len(e) != 0:
            traverse_tree(e, elem_lst)


def extract_text(html_elem, txt_lst):
    for e in html_elem:
        if isinstance(e.tag, basestring):
            if e.tag == 'script':
                continue
            if e.text:
                etext = e.text.strip()
                if len(etext) != 0:
                    txt_lst.append(etext)
            if len(e) != 0:
                extract_text(e, txt_lst)
            if e.tail:
                etext = e.tail.strip()
                if len(etext) != 0:
                    txt_lst.append(etext)


def extract_cleaned_words_iter(html_elem ):
    """

    :param html_elem:
    :return:
    """
    global exclude_words_lst
    for w in number_filter_iter(filter_iter(tolower_iter(extract_words_iter(html_elem)), exclude_words_lst)):
        yield w


def filter_iter(words_lst, exclude_words_lst):
    for w in words_lst:
        if w not in exclude_words_lst:
            yield w


def number_filter_iter(words_lst):
    for w in words_lst:
        if not is_number(w):
            yield w


def tolower_iter(words_lst):
    for w in words_lst:
        yield w.lower()


def extract_words_iter(html_elem):
    """

    :param html_elem:
    :return:
    """
    #words_lst = html_elem.xpath("//text()")
    # for w in words_lst:
    #     print w
    # pass
    for e in html_elem.iter(tag=etree.Element):
        if e.tag == 'script':
            continue
        if e.text and len(e.text.strip()) != 0:
            lst = split_to_words(e.text)
            for w in lst:
                yield w
        if e.tail and len(e.tail.strip()) != 0:
            lst = split_to_words(e.tail.strip())
            for w in lst:
                yield w


def create_words_frequency_dic(words_lst):
    frequency_lst = {}
    for w in words_lst:
        if w in frequency_lst:
            frequency_lst[w] += 1
        else:
            frequency_lst[w] = 1

    return frequency_lst


def create_words_cloud(words_frequency_dic):
    lst = words_frequency_dic.items()
    lst.sort(key=lambda x: x[1])
    lst.reverse()
    return lst


def split_to_words(line):
    words = [w for w in re.split('\W+', line) if len(w) != 0]
    return words


def extend_list(list1, list2):
    if len(list2) != 0:
        list1 += list2


def build_html_tree(html_page_txt):
    """

    :param html_page_txt:
    :return: html tree
    """
    tree = html.fromstring(html_page_txt)
    return tree


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def create_ngram_frequency_dic(words_list, n):
    list_len = len(words_list)
    i = 0
    freq_dic = {}
    while i < list_len - n + 1:
        n_gram = tuple(words_list[i:i+n])
        if n_gram not in freq_dic:
            count = calc_ngram_freq(words_list, n_gram)
            freq_dic[n_gram] = count
        i += 1

    return freq_dic


def create_2gram_frequency_dic(words_list):
    list_len = len(words_list)
    i = 0
    freq_dic = {}
    while i < list_len - 1:
        two_gram = (words_list[i], words_list[i+1])
        if two_gram not in freq_dic:
            count = calc_ngram_freq(words_list, two_gram)
            freq_dic[two_gram] = count
        i += 1

    return freq_dic


def calc_ngram_freq(words_list, ngram):
    ngram_len = len(ngram)

    cnt = 0
    for i in xrange(len(words_list) - ngram_len + 1):
        for j, w in enumerate(ngram):
            if w != words_list[i+j]:
                break
        else:
            cnt += 1

    return cnt


def img_iter(html_elem):
    """

    :param html_elem:
    :return:
    """
    #words_lst = html_elem.xpath("//text()")
    # for w in words_lst:
    #     print w
    # pass
    for e in html_elem.iter('img'):
        # print etree.tostring(e,method='html', pretty_print=True)
        yield e


def img_filter_iter(img_lst):
    for img in img_lst:
        if img.attrib.get('alt', '') == '':
            yield img


def calc_empty_img_alt(img_lst):
    """
    calculate images count which don't have attribute alt or alt is empty string
    :param img_lst:
    :return:
    """
    cnt = 0
    for img in img_lst:
        if img.attrib.get('alt', '') == '':
            cnt += 1

    return cnt


def calc_code_to_text_ratio(html_tree, page_len):
    txt_lst = []
    # extract_text(html_tree, txt_lst)

    for e in html_tree.iter(tag=etree.Element):
        if e.tag == 'script':
            continue
        if e.text and len(e.text.strip()) != 0:
            txt_lst.append(e.text.strip())
        if e.tail and len(e.tail.strip()) != 0:
            txt_lst.append(e.tail.strip())

    text_len = len(''.join(txt_lst))
    ratio = float(text_len)/page_len
    return ratio


def load_indexed_pages(url_str):
    # url_search_template = 'https://www.google.com/search?q=site%%3A%s&rls=com.microsoft:en-US&ie=UTF-8&oe=UTF-8&startIndex=&startPage=1&gws_rd=ssl'
    url_search_template = 'https://www.google.com/search?q=site%%3A%s&gws_rd=ssl'
    search_query = url_search_template % (url_str)
    html = load_page(search_query)
    return html


def load_backlinks(url_str):
    """
    backlinks
    :param url_str:
    :return:
    """
    url_search_template = 'https://www.google.com/search?q=%%22%(url)s%%22-site:%(url)s&gws_rd=ssl'
    search_query = url_search_template % {'url': url_str}
    html = load_page(search_query)
    return html


def load_page(full_url_str):
    request = Request(full_url_str)


    #the result depends on user agent used
    # user_agent = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.103 Safari/537.36'
    # user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'

    request.add_header('User-Agent', user_agent)
    cookie_jar.add_cookie_header(request)
    response = urlopen(request)
    cookie_jar.extract_cookies(response, request)
    html = response.read()
    response.close()
    cookie_jar.save()
    return html


def get_result_stats(html_page_txt):
    """
    :param html_page_txt: html page
    :return:
    """
    tree = html.fromstring(html_page_txt)
    result = tree.find('.//div[@id="resultStats"]')
    """Результатов: примерно 39 600"""
    # extract number
    str = ''.join([i for i in result.text if i in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')])
    if str is not None and len(str) != 0:
        cnt = int(str)
    else:
        cnt = 0
    return cnt


def get_indexed_pages_cnt(url):
    return get_result_stats(load_indexed_pages(url))


def get_backlinks_cnt(url):
    return get_result_stats(load_backlinks(url))


def get_page_rank(url_txt):
    rank = GooglePageRank().get_rank(url_txt)
    return rank


def extract_links(html_tree):
    a_lst = [a.attrib['href'] for a in html_tree.iterfind('.//a')]
    return a_lst


def parse_url(url_txt):
    """
    check the link type: external, internal, inpage, file
        external is lint to other domain or subdomain
        internal is link to other page of the domain
        inpage is link to the same page
        file is link to file
    :param url_txt:
    :return:
    """
    url_txt = url_txt.split('?')[0]  # cut parameters

    if '://' in url_txt:  # external link
        link_type = 'external'
        page_url = url_txt.split('://')[1]
    elif url_txt[0] == '/':  # link to the same top level domain'
        page = url_txt.strip('/').split('/')[-1]  #last item
        if len(page) > 0 and page[0] == '#':
            link_type = 'inpage'
        else:
            link_type = 'internal'
    #TODO: check a link to file

    return link_type


if __name__ == '__main__':
    print get_page_rank('knu.ua')

    # indexed pages count; 37100
    # backlinks count: 6230