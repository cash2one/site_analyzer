#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from appmain import build_html_tree, extract_title, extract_description, traverse_tree, extract_text, \
    extract_heading, extract_cleaned_words_iter, create_words_frequency_dic, create_words_cloud,\
    create_2gram_frequency_dic, calc_ngram_freq, create_ngram_frequency_dic, img_iter, calc_empty_img_alt, \
    img_filter_iter, calc_code_to_text_ratio, extract_links
from htmlpage_utils import load_html_page
import codecs
import os
from lxml import etree
import math
from urllib2 import Request, urlopen
from cookielib import LWPCookieJar
import urllib2
import httplib


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



class PageAnalyzerTest(unittest.TestCase):
    def test_extract_title(self):
        knu_html = load_html_page('Taras Shevchenko National University of Kyiv.htm')
        tree = build_html_tree(knu_html)
        title = extract_title(tree)
        self.assertEqual(title, 'Taras Shevchenko National University of Kyiv')

    def test_extract_descriptiom(self):
        pass
        knu_html = load_html_page('Taras Shevchenko National University of Kyiv.htm')
        tree = build_html_tree(knu_html)
        description = extract_description(tree)
        self.assertIsNone(description)

        head_txt = """
        <head>
        <title>Taras Shevchenko National University of Kyiv</title>
        <link rel="StyleSheet" href="Taras%20Shevchenko%20National%20University%20of%20Kyiv_files/main.css" type="text/css">
        <link rel="alternate" type="application/rss+xml" href="http://knu.ua/ua/test/rss">
        <meta http-equiv="content-type" content="text/html; charset=UTF-8">
        <meta charset="UTF-8">
        <meta name="description" content="This is the site of Taras Shevchenko National University of Kyiv">
        <!-- base href="http://knu.ua/" -->
        <link rel="shortcut icon" href="http://knu.ua/favicon.ico">
        <script src="Taras%20Shevchenko%20National%20University%20of%20Kyiv_files/watch.js" async="" type="text/javascript"></script><script type="text/javascript" src="Taras%20Shevchenko%20National%20University%20of%20Kyiv_files/jquery-1.js"></script>
        </head>
        """

        tree = build_html_tree(head_txt)
        description = extract_description(tree)
        self.assertEqual(description, "This is the site of Taras Shevchenko National University of Kyiv")

    # # def test_traverse_tree(self):
    # #     txt = """<body><h3 class="b-news__title"><a href="http://knu.ua/rss"><img src="Taras%20Shevchenko%20National%20University%20of%20Kyiv_files/rss.gif" title="RSS" align="left"></a>NEWS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</h3></body>"""
    # #     tree = build_html_tree(txt)
    # #     l = []
    # #     traverse_tree(tree, l)
    # #     print l
    # #
    # #     # knu_html = load_html_page('Taras Shevchenko National University of Kyiv.htm')
    # #     # tree = build_html_tree(knu_html)
    # #     # l = []
    # #     # traverse_tree(tree, l)
    # #     # print l
    #
    def test_extract_text(self):
        html_txt = """
        				<div class="b-horizontal-block__also">
						<h4 class="b-horizontal-block__also-title">
							See also
						</h4>
						<ul class="b-horizontal-block__links">
							<li class="b-horizontal-block__link-holder">
								<a href="http://knu.ua/en/geninf/statut/" class="b-horizontal-block__link">
									Statute</a>
								<br>
								<a href="http://knu.ua/en/geninf/ukaz/" class="b-horizontal-block__link">
									Decrees of the President
								</a>
								<br>
								<a href="http://knu.ua/pdfs/official/Lizenzia.pdf" class="b-horizontal-block__link">
									License
								</a>
								<br>
								<a href="http://knu.ua/en/official/accreditation" class="b-horizontal-block__link">
									Certificates of Accreditation
								</a>

								<a href="http://knu.ua/pdfs/Svidotstvo2012.pdf" class="b-horizontal-block__link">
									Certificate to the sign for the goods and services
								</a>
							</li>

						</ul>
					</div>
        """
        lst = []
        tree = build_html_tree(html_txt)
        extract_text(tree, lst)
        rez_lst = ['See also', 'Statute', 'Decrees of the President', 'License', 'Certificates of Accreditation',
                   'Certificate to the sign for the goods and services']
        self.assertListEqual(lst, rez_lst)


        f = open(self.get_html_page_path('Taras Shevchenko National University of Kyiv.htm'), 'r')
        html_txt = f.read()
        f.close()
        tree = build_html_tree(html_txt)
        extract_text(tree, lst)

        # f_output = open('D:\psa\PyCharmPrj\site_analyzer\html_pages\output_taras_shevchenk.txt', 'r')
        f_output = codecs.open(self.get_html_page_path('output_taras_shevchenk.txt'), encoding='utf-8')
        output_lst = [l.strip() for l in f_output]
        f_output.close()
        # FIXME: output list must join some items into one item
        # self.assertListEqual(lst, output_lst)

    def test_extract_heading(self):
        f = open(self.get_html_page_path('Taras Shevchenko National University of Kyiv.htm'), 'r')
        html_txt = f.read()
        f.close()
        tree = build_html_tree(html_txt)
        output = extract_heading(tree)

        headings = [('h3', ['General information']), ('h4', ['See also']), ('h3', ['Official information']),
                    ('h4', ['See also']), ('h3', ['Faculties and Institutes']),
                    ('h4', ['See also']), ('h3', ['For University entrants']), ('h4', ['See also']),
                    ('h3', ['Science']), ('h4', ['See also']), ('h3', ['For students']),
                    ('h4', ['See also']), ('h3', ['Information technologies']), ('h3', ['Resources']),
                    ('h3', ['Libraries']), ('h3', [u'NEWS']), ('h4', ['14.08.2014']), ('h4', ['12.08.2014']),
                    ('h4', ['31.07.2014']), ('h4', ['29.07.2014']), ('h4', ['28.07.2014']),
                    ('h3', ['Favorite Videos']), ('h3', ['International Association Of University']),
                    ('h3', ['University of the Internet']), ('h3', ['Internet radio']), ('h4', ['CAMPUS RADIO'])]

        self.assertListEqual(output, headings)

    def test_extract_words(self):
        f = open(self.get_html_page_path('Taras Shevchenko National University of Kyiv.htm'), 'r')
        html_txt = f.read()
        f.close()
        tree = build_html_tree(html_txt)
        words_lst = [w for w in extract_cleaned_words_iter(tree.find('body'))]
        output_lst = self.convert_lines_to_lst('words-lst.txt')
        self.assertListEqual(words_lst, output_lst)

    def test_create_words_frequency_lst(self):
        f = open(self.get_html_page_path('Taras Shevchenko National University of Kyiv.htm'), 'r')
        html_txt = f.read()
        f.close()
        tree = build_html_tree(html_txt)
        words_lst = extract_cleaned_words_iter(tree.find('body'))
        wfl = create_words_frequency_dic(words_lst)
        #print wfl
        words_cloud = create_words_cloud(wfl)
        etalon_words_cloud = [('university', 26), ('information', 12), ('more', 10), ('students', 9), ('for', 9),
                              ('also', 6), ('about', 6), ('faculties', 6), ('kyiv', 6), ('institutes', 6),
                              ('see', 6), ('academic', 5), (u's', 5), ('is', 5), ('with', 5), ('scientific', 5),
                              ('in', 4), ('science', 4), ('centre', 4), ('ukraine', 4), ('achievements', 4),
                              ('research', 4), ('national', 4), ('educational', 3), ('computer', 3),
                              ('an', 3), ('museum', 3), ('entrants', 3), ('by', 3), ('internet', 3), ('are', 3),
                              ('library', 3), ('resources', 3), (u'degrees', 3), ('staff', 3), ('center', 2),
                              ('student', 2), ('ukrainian', 2), (u'higher', 2), ('as', 2), ('high', 2),
                              ('history', 2), ('newspaper', 2), ('publications', 2), ('official', 2), ('campus', 2),
                              ('observatory', 2), ('search', 2), ('academy', 2), ('halls', 2), ('there', 2),
                              ('electronic', 2), ('sports', 2), ('taras', 2), ('news', 2), ('awards', 2),
                              (u'specialist', 2), ('numerous', 2), ('underpinned', 2), ('maksymovych', 2),
                              ('classical', 2), ('status', 2), ('radio', 2), ('facilities', 2), ('association', 2),
                              ('international', 2), ('has', 2), ('admission', 2), ('sciences', 2), ('shevchenko', 2),
                              ('its', 2), ('arising', 1), ('map', 1), ('organization', 1), ('banks', 1),
                              ('enterprise', 1), ('crimean', 1), ('departments', 1), ('well', 1), ('professor', 1),
                              ('studies', 1), ('branches', 1), ('statute', 1), ('kiev', 1), ('coast', 1),
                              ('president', 1), ('services', 1), ('faculty', 1), ('catalog', 1), (u'phd', 1),
                              (u'qualifications', 1), ('welcome', 1), ('independent', 1), ('profile', 1), ('you', 1),
                              ('department', 1), (u'postgraduate', 1), ('other', 1), ('responsibilities', 1),
                              (u'graduate', 1), ('administration', 1), ('comfortable', 1), ('orders', 1),
                              ('technology', 1), ('education', 1), ('spa', 1), ('have', 1), ('cluster', 1),
                              ('general', 1), ('m', 1), ('classic', 1), ('conferences', 1), (u'reserved', 1),
                              ('pre', 1), ('called', 1), ('ua', 1), ('residence', 1), ('healthy', 1), ('clubs', 1),
                              (u'rights', 1), ('lecture', 1), ('interfaculty', 1), (u'junior', 1), ('technologies', 1),
                              ('particular', 1), ('bidding', 1), (u'thousand', 1), ('hub', 1), ('parliament', 1),
                              ('website', 1), ('today', 1), ('black', 1), (u'master', 1), ('recognised', 1),
                              ('accommodation', 1), ('europe', 1), ('leading', 1), ('distinct', 1), ('area', 1),
                              ('certificate', 1), ('publishing', 1), ('from', 1), ('training', 1), ('unit', 1),
                              (u'post', 1), ('methodological', 1), ('computing', 1), ('hans', 1), ('number', 1),
                              ('within', 1), (u'military', 1), (u'qualification', 1), ('dnipro', 1), ('range', 1),
                              ('union', 1), ('foreign', 1), ('favorite', 1), ('specialized', 1), ('institute', 1),
                              ('license', 1), (u'working', 1), ('lifestyle', 1), ('goods', 1), ('both', 1),
                              ('cafeterias', 1), ('adresses', 1), ('informatics', 1), (u'bachelor', 1),
                              ('continuing', 1), ('zoological', 1), ('rosling', 1), ('email', 1), ('new', 1),
                              ('certificates', 1), ('safety', 1), ('state', 1), ('access', 1), ('academies', 1),
                              ('broad', 1), ('accreditation', 1), ('network', 1), ('primary', 1), ('ru', 1),
                              ('employment', 1), ('crimea', 1), ('decrees', 1), ('sea', 1), ('astrophysical', 1),
                              ('challenges', 1), ('sign', 1), ('phones', 1), ('councils', 1), ('lectures', 1),
                              ('cisco', 1), ('work', 1), ('nationals', 1), ('river', 1), ('facing', 1),
                              ('reprographics', 1), ('prize', 1), (u'school', 1), ('formal', 1), ('provided', 1),
                              ('report', 1), ('nation', 1), (u'overall', 1), ('libraries', 1), ('rules', 1),
                              ('gave', 1), ('local', 1), ('health', 1), ('networking', 1), ('videos', 1),
                              ('geological', 1), ('young', 1), ('periodicals', 1), ('promote', 1), (u'doctoral', 1),
                              ('linguistics', 1), ('rector', 1), ('committee', 1), ('including', 1), ('schools', 1),
                              ('unofficial', 1), ('trade', 1), ('contemporary', 1), ('astronomical', 1),
                              ('radiation', 1), ('dance', 1), ('rectors', 1), (u'all', 1)]

        self.assertListEqual(words_cloud, etalon_words_cloud)

    def test_ngram(self):
        words_list = ['taras', 'shevchenko', 'national', 'university', 'of', 'kyiv', 'is', 'today', 'a', 'classic',
                        'university', 'with', 'a', 'distinct', 'research', 'profile', 'and', 'the', 'leading',
                        'contemporary', 'academic', 'and', 'educational', 'hub', 'of', 'ukraine', 'with', 'the',
                        'independent', 'ukrainian', 'nation', 'arising', 'the', 'university', 'is', 'facing', 'new',
                        'challenges', 'and', 'responsibilities']
        words_list2 = ['profile', 'and', 'the', 'leading',
                        'profile', 'and', 'the', 'leading',
                        'is', 'leading', 'is',
                        'profile', 'and', 'the', 'leading',]

        freq = calc_ngram_freq([], ('the',))
        self.assertEqual(freq, 0)
        freq = calc_ngram_freq(['the'], ('the',))
        self.assertEqual(freq, 1)
        freq = calc_ngram_freq(['the', 'it', 'the', 'education'], ('the',))
        self.assertEqual(freq, 2)
        freq = calc_ngram_freq(['the'], ('the', 'independent'))
        self.assertEqual(freq, 0)
        freq = calc_ngram_freq(['the', 'independent'], ('the', 'independent'))
        self.assertEqual(freq, 1)
        freq = calc_ngram_freq(['the', 'the', 'independent'], ('the', 'independent'))
        self.assertEqual(freq, 1)
        freq = calc_ngram_freq(['taras', 'shevchenko', 'national', 'university', 'of', 'kyiv', 'is', 'today', 'a', 'classic',
                        'university', 'with', 'a', 'distinct', 'research', 'profile', 'and', 'the', 'leading',
                        'contemporary', 'academic', 'and', 'educational', 'hub', 'of', 'ukraine', 'with', 'the',
                        'independent', 'ukrainian', 'nation', 'arising', 'the', 'university', 'is', 'facing', 'new',
                        'challenges', 'and', 'responsibilities',
                        'the', 'independent', 'the', 'independent', 'the'], ('the', 'independent'))
        self.assertEqual(freq, 3)
        freq = calc_ngram_freq(['taras', 'shevchenko', 'national', 'university', 'of', 'kyiv', 'is', 'today', 'a', 'classic',
                        'university', 'with', 'a', 'distinct', 'research', 'profile', 'and', 'the', 'leading',
                        'contemporary', 'academic', 'and', 'educational', 'hub', 'of', 'ukraine', 'with', 'the',
                        'independent', 'ukrainian', 'nation', 'arising', 'the', 'university', 'is', 'facing', 'new',
                        'challenges', 'and', 'responsibilities',
                        'the', 'independent', 'the', 'independent', 'the'], ('the', 'independent', 'ukrainian'))
        self.assertEqual(freq, 1)


        freq_dic = create_2gram_frequency_dic([])
        self.assertDictEqual(freq_dic, {})
        freq_dic = create_2gram_frequency_dic(['the'])
        self.assertDictEqual(freq_dic, {})
        freq_dic = create_2gram_frequency_dic(['is', 'facing'])
        self.assertDictEqual(freq_dic, {('is', 'facing'): 1})
        freq_dic = create_2gram_frequency_dic(['is', 'facing', 'facing'])
        self.assertDictEqual(freq_dic, {('is', 'facing'): 1, ('facing', 'facing'): 1})
        freq_dic = create_2gram_frequency_dic(['is', 'facing', 'is', 'facing'])
        self.assertDictEqual(freq_dic, {('is', 'facing'): 2, ('facing', 'is'): 1})
        freq_dic = create_2gram_frequency_dic(['is', 'facing', 'the', 'is', 'facing'])
        self.assertDictEqual(freq_dic, {('is', 'facing'): 2, ('facing', 'the'): 1, ('the', 'is'): 1})
        freq_dic = create_2gram_frequency_dic(words_list2)
        self.assertDictEqual(freq_dic, {('and', 'the'): 3, ('is', 'leading'): 1, ('is', 'profile'): 1,
                                        ('leading', 'is'): 2, ('leading', 'profile'): 1,
                                        ('profile', 'and'): 3, ('the', 'leading'): 3})

        freq_dic = create_ngram_frequency_dic([], 3)
        self.assertDictEqual(freq_dic, {})
        freq_dic = create_ngram_frequency_dic(['the'], 3)
        self.assertDictEqual(freq_dic, {})
        freq_dic = create_ngram_frequency_dic(['is', 'facing', 'it'], 3)
        self.assertDictEqual(freq_dic, {('is', 'facing', 'it'): 1})
        freq_dic = create_ngram_frequency_dic(['is', 'facing', 'facing', 'facing'], 3)
        self.assertDictEqual(freq_dic, {('is', 'facing', 'facing'): 1, ('facing', 'facing', 'facing'): 1})
        freq_dic = create_ngram_frequency_dic(['is', 'facing', 'is', 'facing', 'is'], 3)
        self.assertDictEqual(freq_dic, {('is', 'facing', 'is'): 2, ('facing', 'is', 'facing'): 1})
        freq_dic = create_ngram_frequency_dic(['is', 'facing', 'the', 'is', 'facing', 'the'], 3)
        self.assertDictEqual(freq_dic, {('is', 'facing', 'the'): 2, ('facing', 'the', 'is'): 1, ('the', 'is', 'facing'): 1})
        freq_dic = create_ngram_frequency_dic(words_list2, 2)
        self.assertDictEqual(freq_dic, {('and', 'the'): 3, ('is', 'leading'): 1, ('is', 'profile'): 1,
                                        ('leading', 'is'): 2, ('leading', 'profile'): 1,
                                        ('profile', 'and'): 3, ('the', 'leading'): 3})

        freq_dic = create_ngram_frequency_dic(words_list2, 3)
        self.assertDictEqual(freq_dic, {('and', 'the', 'leading'): 3,
                                        ('is', 'leading', 'is'): 1,
                                        ('is', 'profile', 'and'): 1,
                                        ('leading', 'is', 'leading'): 1,
                                        ('leading', 'is', 'profile'): 1,
                                        ('leading', 'profile', 'and'): 1,
                                        ('profile', 'and', 'the'): 3,
                                        ('the', 'leading', 'is'): 1,
                                        ('the', 'leading', 'profile'): 1}

                             )

    def test_extract_img_iter(self):
        f = open(self.get_html_page_path('Taras Shevchenko National University of Kyiv.htm'), 'r')
        html_txt = f.read()
        f.close()
        tree = build_html_tree(html_txt)
        # l = [etree.tostring(item,method='html', pretty_print=True) for item in extract_img_iter(tree.find('body'))]
        l = [item for item in img_iter(tree.find('body'))]

        img_lst = ['<img src="Taras%20Shevchenko%20National%20University%20of%20Kyiv_files/rss.gif" title="RSS" align="left">\n',
         '<img src="Taras%20Shevchenko%20National%20University%20of%20Kyiv_files/10.jpg">\n  \n',
         '<img src="Taras%20Shevchenko%20National%20University%20of%20Kyiv_files/9.jpg">\n  \n',
         '<img src="Taras%20Shevchenko%20National%20University%20of%20Kyiv_files/8.jpg">\n  \n',
         '<img src="Taras%20Shevchenko%20National%20University%20of%20Kyiv_files/3.jpg">\n  \n',
         '<img src="Taras%20Shevchenko%20National%20University%20of%20Kyiv_files/4.jpg">\n  \n',
         '<img src="Taras%20Shevchenko%20National%20University%20of%20Kyiv_files/178e.jpg" alt="" class="b-gallery__video">\n\t\t\t\t\t\n',
         '<img src="Taras%20Shevchenko%20National%20University%20of%20Kyiv_files/observ.jpg" alt="" height="63" width="142">\n\t\t\t\t\t\n',
         '<img src="Taras%20Shevchenko%20National%20University%20of%20Kyiv_files/iau.jpg" alt="" height="63" width="142">\n\t\t\t\t\t\n',
         '<img src="Taras%20Shevchenko%20National%20University%20of%20Kyiv_files/eua.jpg" height="63" width="142">\n',
         '<img src="Taras%20Shevchenko%20National%20University%20of%20Kyiv_files/euroasian.jpg" alt="" border="0" height="63" width="142">\n\t\t\t\t\t\n',
         '<img src="Taras%20Shevchenko%20National%20University%20of%20Kyiv_files/een.jpg" title="EEN" alt="EEN" border="0" '
            'height="120" hspace="2" vspace="2" width="160">\n',
         '<img src="Taras%20Shevchenko%20National%20University%20of%20Kyiv_files/monBaner.jpg" alt="&#1052;&#1054;&#1053;" border="0" hspace="2">\n',
         '<img src="Taras%20Shevchenko%20National%20University%20of%20Kyiv_files/fbBaner.gif" alt="&#1052;&#1054;&#1053;" border="0">\n',
         '<img src="Taras%20Shevchenko%20National%20University%20of%20Kyiv_files/vnz.png" title="&#1042;&#1080;&#1097;'
            '&#1072; &#1086;&#1089;&#1074;&#1110;&#1090;&#1072;" alt="&#1042;&#1080;&#1097;&#1072; &#1086;&#1089;&#1074;'
            '&#1110;&#1090;&#1072;" border="0" height="60" hspace="2" vspace="2" width="180">\n',
         '<img src="Taras%20Shevchenko%20National%20University%20of%20Kyiv_files/qs.png" title="World University Rankings" '
            'alt="World University Rankings" border="0" vspace="2">\n',
         '<img src="Taras%20Shevchenko%20National%20University%20of%20Kyiv_files/compas_banner.png" title="Best '
            'Universities" alt="Best Universities" border="0" height="140" hspace="2" vspace="2" width="96">\n',
         '<img src="Taras%20Shevchenko%20National%20University%20of%20Kyiv_files/radio.jpg" alt="" class="b-triplet__img_type_radio">\n\t\t\t\t\t\n',
         '<img src="Taras%20Shevchenko%20National%20University%20of%20Kyiv_files/gerb3.png" alt="" class="b-foot__emblem">\n\t\t\n',
         '<img src="//mc.yandex.ru/watch/20542042" style="position:absolute; left:-9999px;" alt="">\n']

        self.assertListEqual([etree.tostring(item,method='html', pretty_print=True) for item in l], img_lst)
        cnt = len(list(img_filter_iter(img_iter(tree.find('body')))))
        # cnt = calc_empty_img_alt(img_iter(tree.find('body')))
        self.assertEqual(cnt, 14)

    def test_code_to_text_ratio(self):
        f = open(self.get_html_page_path('Taras Shevchenko National University of Kyiv.htm'), 'r')
        html_txt = f.read()
        f.close()
        tree = build_html_tree(html_txt)
        body = tree.find('body')
        ratio = calc_code_to_text_ratio(body, len(html_txt))
        self.assertEqual(math.ceil(ratio*100)/100, 0.16)

    def test_extract_links(self):
        html_page = self.load_page('http://knu.ua')
        # f = open(self.get_html_page_path('Taras Shevchenko National University of Kyiv.htm'), 'r')
        # html_txt = f.read()
        # f.close()

        tree = build_html_tree(html_page)
        body = tree.find('body')
        links = extract_links(tree)
        pass

    def get_html_page_path(self, page_name):
        html_dir = self.get_html_pages_dir()
        page_path = os.path.join(html_dir, page_name)
        return page_path

    def get_html_pages_dir(self):
        cur_path = os.path.realpath(__file__)
        dir_path =  os.path.dirname(os.path.dirname(cur_path))
        html_pages_dir = os.path.join(dir_path, 'html_pages')
        return html_pages_dir

    def convert_lines_to_lst(self, f_name):
        f_output = codecs.open(self.get_html_page_path(f_name), encoding='utf-8')
        output_lst = [l.strip() for l in f_output]
        f_output.close()
        return  output_lst

    def load_page(self, url_txt):
        opener = urllib2.build_opener()
        opener.addheaders = [("User-agent", "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                            "Chrome/37.0.2062.103 Safari/537.36")]
        response = opener.open(url_txt, timeout=30)
        if response.getcode() == httplib.OK:
            html_page = response.read()
        else:
            html_page = None

        return html_page


#lst.sort(key=lambda x: x[1])
# lst.reverse()
# sorted(lst, ...
if __name__ == '__main__':
    unittest.main()