#!/usr/bin/env python3
# -*- coding: utf-8 -*
"""
Searching and Downloading Google Images to the local disk
"""
import argparse
import codecs
import datetime
import http.client
import json
import logging
import os
import ssl
# Import Libraries
import sys
import urllib.request
from time import sleep, perf_counter  # Importing the time library to check the time of code execution
from urllib.parse import quote
from urllib.request import Request, urlopen, URLError, HTTPError

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

logging.basicConfig(filename='google-images-download.log',
                    level=logging.INFO, format="%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s")

http.client._MAXHEADERS = 1000

ARGS_LIST = ["keywords", "keywords_from_file", "prefix_keywords", "suffix_keywords",
             "limit", "format", "color", "color_type", "usage_rights", "size",
             "exact_size", "aspect_ratio", "type", "time", "time_range", "delay", "url", "single_image",
             "output_directory", "image_directory", "no_directory", "proxy", "similar_images", "specific_site",
             "print_urls", "print_size", "print_paths", "metadata", "extract_metadata", "socket_timeout",
             "thumbnail", "language", "prefix", "chrome_driver_path", "related_images", "safe_search", "no_numbering",
             "offset", "no_download"]


def user_input():
    """
    Parse the configuration file of the arguments passed in command line. Behavior based of the configuration file
       specified in command line or programmatically in a python script.
       :return: A list of parameter that configure the application.
    """
    config = argparse.ArgumentParser()
    config.add_argument('-cf', '--config_file', help='config file name', default='', type=str, required=False)
    config_file_check = config.parse_known_args()
    object_check = vars(config_file_check[0])

    if object_check['config_file'] != '':
        records = []
        json_file = json.load(open(config_file_check[0].config_file))
        for record in range(0, len(json_file['Records'])):
            arguments = {}
            for i in ARGS_LIST:
                arguments[i] = None
            for key, value in json_file['Records'][record].items():
                arguments[key] = value
            records.append(arguments)
    else:
        # Taking command line arguments from users
        parser = argparse.ArgumentParser()
        parser.add_argument('-k', '--keywords', help='Delimited list input', type=str, required=False)
        parser.add_argument('-kf', '--keywords_from_file', help='extract list of keywords from a text file', type=str,
                            required=False)
        parser.add_argument('-sk', '--suffix_keywords',
                            help='Comma separated additional words added after to main keyword', type=str,
                            required=False)
        parser.add_argument('-pk', '--prefix_keywords',
                            help='Comma separated additional words added before main keyword', type=str, required=False)
        parser.add_argument('-l', '--limit', help='Delimited list input', type=str, required=False)
        parser.add_argument('-f', '--format', help='Download images with specific format', type=str, required=False,
                            choices=['jpg', 'gif', 'png', 'bmp', 'svg', 'webp', 'ico'])
        parser.add_argument('-u', '--url', help='Search with google image URL', type=str, required=False)
        parser.add_argument('-x', '--single_image', help='Downloading a single image from URL', type=str,
                            required=False)
        parser.add_argument('-o', '--output_directory', help='Download images in a specific main directory', type=str,
                            required=False)
        parser.add_argument('-i', '--image_directory', help='Download images in a specific sub-directory', type=str,
                            required=False)
        parser.add_argument('-n', '--no_directory', default=False,
                            help='Download images in the main directory but no sub-directory', action="store_true")
        parser.add_argument('-d', '--delay', help='Delay in seconds to wait between downloading two images', type=int,
                            required=False)
        parser.add_argument('-co', '--color', help='Filter on color', type=str, required=False,
                            choices=['red', 'orange', 'yellow', 'green', 'teal', 'blue', 'purple', 'pink', 'white',
                                     'gray', 'black', 'brown'])
        parser.add_argument('-ct', '--color_type', help='Filter on color', type=str, required=False,
                            choices=['full-color', 'black-and-white', 'transparent'])
        parser.add_argument('-r', '--usage_rights', help='Usage rights', type=str, required=False,
                            choices=['labeled-for-reuse-with-modifications', 'labeled-for-reuse',
                                     'labeled-for-noncommercial-reuse-with-modification',
                                     'labeled-for-nocommercial-reuse'])
        parser.add_argument('-s', '--size', help='Image size', type=str, required=False,
                            choices=['large', 'medium', 'icon', '>400*300', '>640*480', '>800*600', '>1024*768', '>2MP',
                                     '>4MP', '>6MP', '>8MP', '>10MP', '>12MP', '>15MP', '>20MP', '>40MP', '>70MP'])
        parser.add_argument('-es', '--exact_size', help='Exact image resolution "WIDTH,HEIGHT"', type=str,
                            required=False)
        parser.add_argument('-t', '--type', help='Image type', type=str, required=False,
                            choices=['face', 'photo', 'clipart', 'line-drawing', 'animated'])
        parser.add_argument('-w', '--time', help='Image age', type=str, required=False,
                            choices=['past-24-hours', 'past-7-days'])
        parser.add_argument('-wr', '--time_range',
                            help="""time range for the age of the image. should be in the format \n
                            {"time_min":"MM/DD/YYYY","time_max":"MM/DD/YYYY"}""",
                            type=str, required=False)
        parser.add_argument('-a', '--aspect_ratio', help='Comma separated additional words added to keywords', type=str,
                            required=False,
                            choices=['tall', 'square', 'wide', 'panoramic'])
        parser.add_argument('-si', '--similar_images',
                            help='Downloads images very similar to the image URL you provide', type=str, required=False)
        parser.add_argument('-ss', '--specific_site', help='Downloads images that are indexed from a specific website',
                            type=str, required=False)
        parser.add_argument('-p', '--print_urls', default=False, help="Print the URLs of the images",
                            action="store_true")
        parser.add_argument('-ps', '--print_size', default=False, help="Print the size of the images on disk",
                            action="store_true")
        parser.add_argument('-pp', '--print_paths', default=False,
                            help="Prints the list of absolute paths of the images", action="store_true")
        parser.add_argument('-m', '--metadata', default=False, help="Print the metadata of the image",
                            action="store_true")
        parser.add_argument('-e', '--extract_metadata', default=False, help="Dumps all the logs into a text file",
                            action="store_true")
        parser.add_argument('-st', '--socket_timeout', default=False,
                            help="Connection timeout waiting for the image to download", type=float)
        parser.add_argument('-th', '--thumbnail', default=False,
                            help="Downloads image thumbnail along with the actual image", action="store_true")
        parser.add_argument('-la', '--language', default=False,
                            help="Defines the language filter. The search results are authomatically returned in that language",
                            type=str, required=False,
                            choices=['Arabic', 'Chinese (Simplified)', 'Chinese (Traditional)', 'Czech', 'Danish',
                                     'Dutch', 'English', 'Estonian', 'Finnish', 'French', 'German', 'Greek', 'Hebrew',
                                     'Hungarian', 'Icelandic', 'Italian', 'Japanese', 'Korean', 'Latvian', 'Lithuanian',
                                     'Norwegian', 'Portuguese', 'Polish', 'Romanian', 'Russian', 'Spanish', 'Swedish',
                                     'Turkish'])
        parser.add_argument('-pr', '--prefix', default=False,
                            help="A word that you would want to prefix in front of each image name", type=str,
                            required=False)
        parser.add_argument('-px', '--proxy', help='specify a proxy address and port', type=str, required=False)
        parser.add_argument('-cd', '--chrome_driver_path',
                            help='specify the path to chrome_driver_path executable in your local machine', type=str,
                            required=False)
        parser.add_argument('-ri', '--related_images', default=False,
                            help="Downloads images that are similar to the keyword provided", action="store_true")
        parser.add_argument('-sa', '--safe_search', default=False,
                            help="Turns on the safe search filter while searching for images", action="store_true")
        parser.add_argument('-nn', '--no_numbering', default=False,
                            help="Allows you to exclude the default numbering of images", action="store_true")
        parser.add_argument('-of', '--offset', help="Where to start in the fetched links", type=str, required=False)
        parser.add_argument('-nd', '--no_download', default=False,
                            help="Prints the URLs of the images and/or thumbnails without downloading them",
                            action="store_true")

        args = parser.parse_args()
        arguments = vars(args)
        records = []
        records.append(arguments)
    return records


class GoogleImageDownloadException(Exception):
    """
    Specific exception of the GoogleImageDownload class.
    """
    pass


class GoogleImageDownload:
    """
    Main class of this data creator. The one to call directly within a script.
    """

    def __init__(self, argument_or_configuration):
        """
        Constructor of the main class taking the configuration of any download.
           :parameter argument_or_configuration: Arguments programmaticaly passed or from arguments in config file.
        """
        if isinstance(argument_or_configuration, dict) is True:
            self.configuration = argument_or_configuration
        else:
            raise TypeError("Configuration passed to to the constructor must be dict type.")

    @staticmethod
    def download_page(url):
        """
        Downloading entire Web Document (Raw Page Content).
           :parameter url: URL of tha page.
           :return: Source code the page.
        """
        try:
            headers = {}
            headers[
                'User-Agent'] \
                = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
            req = urllib.request.Request(url, headers=headers)
            resp = urllib.request.urlopen(req)
            response_data = str(resp.read())
            return response_data
        except Exception as error:
            logging.warning(
                "Could not open URL. Please check your internet connection and/or ssl settings, error message is: %s" %
                str(error))

    @staticmethod
    def download_extended_page(url, chrome_driver_path):
        """
        If more than 100 image are downloaded.
           :parameter url: Page URL to parse
           :parameter chrome_driver_path: Path to the chrome driver
           :return: Page source
        """
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument("--headless")

        try:
            browser = webdriver.Chrome(chrome_driver_path, chrome_options=options)
        except Exception as error:
            logging.warning(
                "Fail to locate the chrome driver 'chrome_driver_path', error message is: %s"% str(error))
            sys.exit()
        browser.set_window_size(1024, 768)

        # Open the link
        browser.get(url)
        sleep(1)
        logging.info("Getting you a lot of images. This may take a few moments...")

        element = browser.find_element_by_tag_name("body")
        # Scroll down
        for _ in range(30):
            element.send_keys(Keys.PAGE_DOWN)
            sleep(0.3)

        try:
            browser.find_element_by_id("smb").click()
            for _ in range(50):
                element.send_keys(Keys.PAGE_DOWN)
                sleep(0.3)  # bot id protection
        except Exception:
            for _ in range(10):
                element.send_keys(Keys.PAGE_DOWN)
                sleep(0.3)  # bot id protection

        logging.info("Reached end of Page.")
        sleep(0.5)

        source = browser.page_source  # page source
        # close the browser
        browser.close()

        return source

    @staticmethod
    def get_next_tab(source):
        """
        Finding 'Next Image' from the given raw page
           :parameter source: Source of the URL.
           :return: A tuple made of the URL of the item, it's name and the end content.
        """
        start_line = source.find('class="dtviD"')
        if start_line == -1:  # If no links are found then give an error!
            end_quote = 0
            link = "no_tabs"
            return link, '', end_quote
        else:
            start_line = source.find('class="dtviD"')
            start_content = source.find('href="', start_line + 1)
            end_content = source.find('">', start_content + 1)
            url_item = "https://www.google.com" + str(source[start_content + 6:end_content])
            url_item = url_item.replace('&amp;', '&')

            start_line_2 = source.find('class="dtviD"')
            start_content_2 = source.find(':', start_line_2 + 1)
            end_content_2 = source.find('"', start_content_2 + 1)
            url_item_name = str(source[start_content_2 + 1:end_content_2])

            return url_item, url_item_name, end_content

    @staticmethod
    def get_all_tabs(page):
        """
        Getting all links with the help of '_images_get_next_image'.
           :parameter page: Page to parse.
           :return: Link in the page.
        """
        tabs = {}
        while True:
            item, item_name, end_content = GoogleImageDownload.get_next_tab(page)
            if item == "no_tabs":
                break
            else:
                tabs[item_name] = item  # Append all the links in the list named 'Links'
                sleep(0.1)  # Timer could be used to slow down the request for image downloads
                page = page[end_content:]
        return tabs

    @staticmethod
    def format_object(object_2_format):
        """
        Format the object in readable format
           :parameter object_2_format: Object to format.
           :return: The formatted object.
        """
        formatted_object = {}
        formatted_object['image_format'] = object_2_format['ity']
        formatted_object['image_height'] = object_2_format['oh']
        formatted_object['image_width'] = object_2_format['ow']
        formatted_object['image_link'] = object_2_format['ou']
        formatted_object['image_description'] = object_2_format['pt']
        formatted_object['image_host'] = object_2_format['rh']
        formatted_object['image_source'] = object_2_format['ru']
        formatted_object['image_thumbnail_url'] = object_2_format['tu']
        return formatted_object

    @staticmethod
    def single_image(image_url):
        """
        Function to download single image.
           :parameter image_url: URL of the image.
           :return: Nothing to be returned.
        """
        main_directory = "downloads"
        extensions = (".jpg", ".gif", ".png", ".bmp", ".svg", ".webp", ".ico")
        url = image_url
        try:
            os.makedirs(main_directory)
        except OSError as error:
            if error.errno != 17:
                raise
            pass
        req = Request(url, headers={
            "User-Agent"
            : "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})

        response = urlopen(req, None, 10)
        data = response.read()
        response.close()

        image_name = str(url[(url.rfind('/')) + 1:])
        if '?' in image_name:
            image_name = image_name[:image_name.find('?')]
        if any(map(lambda extension: extension in image_name, extensions)):
            file_name = main_directory + "/" + image_name
        else:
            file_name = main_directory + "/" + image_name + ".jpg"
            image_name = image_name + ".jpg"

        output_file = open(file_name, 'wb')
        output_file.write(data)
        output_file.close()

        logging.info("completed ====> %s" % image_name)
        return

    @staticmethod
    def similar_images(similar_images):
        """
        Find images to download with a URL as reference instead of a keyword.
           :parameter similar_images: URL
           :return: URL content.
        """
        try:
            search_url = 'https://www.google.com/searchbyimage?site=search&sa=X&image_url=' + similar_images
            headers = {}
            headers[
                'User-Agent'] \
                = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"

            req1 = urllib.request.Request(search_url, headers=headers)
            resp1 = urllib.request.urlopen(req1)
            content = str(resp1.read())

            length_3 = content.find('/search?sa=X&amp;q=')
            length_4 = content.find(';', length_3 + 19)
            url = content[length_3 + 19:length_4]
            return url
        except Exception:
            return "Could not connect to Google Images endpoint"

    def build_url_parameters(self):
        """
        Building URL parameters.
           :return: The URL.
        """
        if self.configuration['language']:
            lang = "&lr="
            lang_param = {"Arabic": "lang_ar", "Chinese (Simplified)": "lang_zh-CN",
                          "Chinese (Traditional)": "lang_zh-TW", "Czech": "lang_cs", "Danish": "lang_da",
                          "Dutch": "lang_nl", "English": "lang_en", "Estonian": "lang_et", "Finnish": "lang_fi",
                          "French": "lang_fr", "German": "lang_de", "Greek": "lang_el", "Hebrew": "lang_iw ",
                          "Hungarian": "lang_hu", "Icelandic": "lang_is", "Italian": "lang_it", "Japanese": "lang_ja",
                          "Korean": "lang_ko", "Latvian": "lang_lv", "Lithuanian": "lang_lt", "Norwegian": "lang_no",
                          "Portuguese": "lang_pt", "Polish": "lang_pl", "Romanian": "lang_ro", "Russian": "lang_ru",
                          "Spanish": "lang_es", "Swedish": "lang_sv", "Turkish": "lang_tr"}
            lang_url = lang + lang_param[self.configuration['language']]
        else:
            lang_url = ''

        if self.configuration['time_range']:
            time_range = ',cdr:1,cd_min:' + self.configuration['time_range']['time_min'] \
                         + ',cd_max:' + self.configuration['time_range']['time_max']
        else:
            time_range = ''

        if self.configuration['exact_size']:
            size_array = [x.strip() for x in self.configuration['exact_size'].split(',')]
            exact_size = ",isz:ex,iszw:" + str(size_array[0]) + ",iszh:" + str(size_array[1])
        else:
            exact_size = ''

        built_url = "&tbs="
        counter = 0
        params = {
            'color': [self.configuration['color'], {'red': 'ic:specific,isc:red', 'orange': 'ic:specific,isc:orange',
                                                    'yellow': 'ic:specific,isc:yellow',
                                                    'green': 'ic:specific,isc:green',
                                                    'teal': 'ic:specific,isc:teel', 'blue': 'ic:specific,isc:blue',
                                                    'purple': 'ic:specific,isc:purple', 'pink': 'ic:specific,isc:pink',
                                                    'white': 'ic:specific,isc:white', 'gray': 'ic:specific,isc:gray',
                                                    'black': 'ic:specific,isc:black',
                                                    'brown': 'ic:specific,isc:brown'}],
            'color_type': [self.configuration['color_type'],
                           {'full-color': 'ic:color', 'black-and-white': 'ic:gray', 'transparent': 'ic:trans'}],
            'usage_rights': [self.configuration['usage_rights'],
                             {'labeled-for-reuse-with-modifications': 'sur:fmc', 'labeled-for-reuse': 'sur:fc',
                              'labeled-for-noncommercial-reuse-with-modification': 'sur:fm',
                              'labeled-for-nocommercial-reuse': 'sur:f'}],
            'size': [self.configuration['size'],
                     {'large': 'isz:l', 'medium': 'isz:m', 'icon': 'isz:i', '>400*300': 'isz:lt,islt:qsvga',
                      '>640*480': 'isz:lt,islt:vga', '>800*600': 'isz:lt,islt:svga',
                      '>1024*768': 'visz:lt,islt:xga', '>2MP': 'isz:lt,islt:2mp', '>4MP': 'isz:lt,islt:4mp',
                      '>6MP': 'isz:lt,islt:6mp', '>8MP': 'isz:lt,islt:8mp', '>10MP': 'isz:lt,islt:10mp',
                      '>12MP': 'isz:lt,islt:12mp', '>15MP': 'isz:lt,islt:15mp', '>20MP': 'isz:lt,islt:20mp',
                      '>40MP': 'isz:lt,islt:40mp', '>70MP': 'isz:lt,islt:70mp'}],
            'type': [self.configuration['type'], {'face': 'itp:face', 'photo': 'itp:photo', 'clipart': 'itp:clipart',
                                                  'line-drawing': 'itp:lineart', 'animated': 'itp:animated'}],
            'time': [self.configuration['time'], {'past-24-hours': 'qdr:d', 'past-7-days': 'qdr:w'}],
            'aspect_ratio': [self.configuration['aspect_ratio'],
                             {'tall': 'iar:t', 'square': 'iar:s', 'wide': 'iar:w', 'panoramic': 'iar:xw'}],
            'format': [self.configuration['format'],
                       {'jpg': 'ift:jpg', 'gif': 'ift:gif', 'png': 'ift:png', 'bmp': 'ift:bmp', 'svg': 'ift:svg',
                        'webp': 'webp', 'ico': 'ift:ico'}]}
        for _, value in params.items():
            if value[0] is not None:
                ext_param = value[1][value[0]]
                # counter will tell if it is first param added or not
                if counter == 0:
                    # add it to the built url
                    built_url = built_url + ext_param
                    counter += 1
                else:
                    built_url = built_url + ',' + ext_param
                    counter += 1
        built_url = lang_url + built_url + exact_size + time_range
        return built_url

    def build_search_url(self, search_term, params, url, similar_images, specific_site, safe_search):
        """
        Building main search URL.
           :parameter search_term: Term to search.
           :parameter params: parameters of the search.
           :parameter url: URL to search.
           :parameter similar_images: Image to base the search on.
           :parameter specific_site: Search on that specific site.
           :parameter safe_search: Safe search of google.
           :return: The created URL.
        """
        # check safe_search
        safe_search_string = "&safe=active"
        # check the args and choose the URL
        if url:
            url = url
        elif similar_images:
            logging.info(similar_images)
            keyword = self.similar_images(similar_images)
            url = 'https://www.google.com/search?q=' \
                  + keyword \
                  + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
        elif specific_site:
            url = 'https://www.google.com/search?q=' + quote(
                search_term) \
                  + '&as_sitesearch=' \
                  + specific_site \
                  + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch' \
                  + params \
                  + '&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
        else:
            url = 'https://www.google.com/search?q=' + quote(
                search_term) \
                  + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch' \
                  + params \
                  + '&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'

        # safe search check
        if safe_search:
            url = url + safe_search_string

        # print(url)
        return url

    @staticmethod
    def file_size(file_path):
        """
        Measures the file size of the downloaded images.
           :parameter file_path: File path of the download images.
           :return: A string representing the size.
        """
        if os.path.isfile(file_path):
            file_info = os.stat(file_path)
            size = file_info.st_size
            for size_unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
                if size < 1024.0:
                    return "%3.1f %s" % (size, size_unit)
                size /= 1024.0
            return size

    @staticmethod
    def keywords_from_file(file_name):
        """
        Retrieve a keyword from a file.
           :parameter file_name: String of the image file name.
           :return: A string representing the keyword.
        """
        search_keyword = []
        with codecs.open(file_name, 'r', encoding='utf-8-sig') as keyword_file:
            if '.csv' in file_name:
                for line in keyword_file:
                    if line in ['\n', '\r\n']:
                        pass
                    else:
                        search_keyword.append(line.replace('\n', '').replace('\r', ''))
            elif '.txt' in file_name:
                for line in keyword_file:
                    if line in ['\n', '\r\n']:
                        pass
                    else:
                        search_keyword.append(line.replace('\n', '').replace('\r', ''))
            else:
                logging.warning("Invalid file type: Valid file types are either .txt or .csv exiting...")
                sys.exit()
        return search_keyword

    @staticmethod
    def create_directories(main_directory, dir_name, thumbnail):
        """
        Create directories based on the arguments.
           :parameter main_directory: Main directory where all the images are based.
           :parameter dir_name: Subdirectory where images are classified by keyword.
           :parameter thumbnail: Subdirectory for thumbnail.
           :return: Nothing to be returned.
        """
        dir_name_thumbnail = dir_name + " - thumbnail"
        # make a search keyword  directory
        try:
            if not os.path.exists(main_directory):
                os.makedirs(main_directory)
                sleep(0.2)
                path = str(dir_name)
                sub_directory = os.path.join(main_directory, path)
                if not os.path.exists(sub_directory):
                    os.makedirs(sub_directory)
                if thumbnail:
                    sub_directory_thumbnail = os.path.join(main_directory, dir_name_thumbnail)
                    if not os.path.exists(sub_directory_thumbnail):
                        os.makedirs(sub_directory_thumbnail)
            else:
                path = str(dir_name)
                sub_directory = os.path.join(main_directory, path)
                if not os.path.exists(sub_directory):
                    os.makedirs(sub_directory)
                if thumbnail:
                    sub_directory_thumbnail = os.path.join(main_directory, dir_name_thumbnail)
                    if not os.path.exists(sub_directory_thumbnail):
                        os.makedirs(sub_directory_thumbnail)
        except OSError as error:
            if error.errno != 17:
                raise
                # sleep might help here
            pass
        return

    @staticmethod
    def download_image_thumbnail(image_url, main_directory, dir_name, return_image_name, print_urls,
                                 socket_timeout, print_size, no_download):
        """
        Download the image thumbnail.
           :parameter image_url: URL of the image.
           :parameter main_directory: Main directory where all the images are saved.
           :parameter dir_name: Name of the subdirectory based on a keyword.
           :parameter return_image_name: Name of the image.
           :parameter print_urls: Argument for printing the URL or not.
           :parameter socket_timeout: Timeout of the socket.
           :parameter print_size: Argument for printing the size or not.
           :parameter no_download: Number of download.
           :return: A tuple made of the download status and the downlaod message.
        """
        if print_urls or no_download:
            logging.info("Image URL: %s" % image_url)
        if no_download:
            return "success", "Printed url without downloading"
        try:
            req = Request(image_url, headers={
                "User-Agent":
                    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
            try:
                # timeout time to download an image
                if socket_timeout:
                    timeout = float(socket_timeout)
                else:
                    timeout = 10

                response = urlopen(req, None, timeout)
                data = response.read()
                response.close()

                path = main_directory + "/" + dir_name + " - thumbnail" + "/" + return_image_name

                try:
                    output_file = open(path, 'wb')
                    output_file.write(data)
                    output_file.close()
                    download_status = 'success'
                    download_message = "Completed Image Thumbnail ====> " + return_image_name
                except OSError as error:
                    download_status = 'fail'
                    download_message = "OSError on an image...trying next one..." + " Error: " + str(error)
                except IOError as error:
                    download_status = 'fail'
                    download_message = "IOError on an image...trying next one..." + " Error: " + str(error)

                # image size parameter
                if print_size:
                    logging.info("Image Size: %s" % str(GoogleImageDownload.file_size(path)))

            except UnicodeEncodeError as error:
                download_status = 'fail'
                download_message = "UnicodeEncodeError on an image...trying next one..." + " Error: " + str(error)

        except HTTPError as error:  # If there is any HTTPError
            download_status = 'fail'
            download_message = "HTTPError on an image...trying next one..." + " Error: " + str(error)

        except URLError as error:
            download_status = 'fail'
            download_message = "URLError on an image...trying next one..." + " Error: " + str(error)

        except ssl.CertificateError as error:
            download_status = 'fail'
            download_message = "CertificateError on an image...trying next one..." + " Error: " + str(error)

        except IOError as error:  # If there is any IOError
            download_status = 'fail'
            download_message = "IOError on an image...trying next one..." + " Error: " + str(error)
        return download_status, download_message

    @staticmethod
    def download_image(image_url, image_format, main_directory, dir_name, count, print_urls, socket_timeout,
                       prefix, print_size, no_numbering, no_download):
        """
        Download image from google image page.
           :parameter image_url: URL of the image.
           :parameter image_format: Format of the image.
           :parameter main_directory: Main directory where all the image are stored.
           :parameter dir_name: Subdirectory where images are classified by keyword.
           :parameter count: Counter of the number of images.
           :parameter print_urls: Argument for printing the URL of the image or not.
           :parameter socket_timeout: Timeout to close connection.
           :parameter prefix: Prefix the image name.
           :parameter print_size: Argument for printing the size of the image or not.
           :parameter no_numbering: Adding the number in the image name or not.
           :parameter no_download: Argument defining if the image is to be downloaded or not.
           :return: A tuple made of the download status, the download message, the image name and the absolute path.
        """
        if print_urls or no_download:
            logging.info("Image URL: %s" % image_url)
        if no_download:
            return "success", "Printed url without downloading", None, None
        try:
            req = Request(image_url, headers={
                "User-Agent":
                    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
            try:
                # timeout time to download an image
                if socket_timeout:
                    timeout = float(socket_timeout)
                else:
                    timeout = 10

                response = urlopen(req, None, timeout)
                data = response.read()
                response.close()

                # keep everything after the last '/'
                image_name = str(image_url[(image_url.rfind('/')) + 1:])
                image_name = image_name.lower()
                # if no extension then add it
                # remove everything after the image name
                if image_format == "":
                    image_name = image_name + "." + "jpg"
                elif image_format == "jpeg":
                    image_name = image_name[:image_name.find(image_format) + 4]
                else:
                    image_name = image_name[:image_name.find(image_format) + 3]

                # prefix name in image
                if prefix:
                    prefix = prefix + " "
                else:
                    prefix = ''

                if no_numbering:
                    path = main_directory + "/" + dir_name + "/" + prefix + image_name
                else:
                    path = main_directory + "/" + dir_name + "/" + prefix + str(count) + "_ " + image_name

                try:
                    output_file = open(path, 'wb')
                    output_file.write(data)
                    output_file.close()
                    absolute_path = os.path.abspath(path)
                except OSError:
                    absolute_path = ''

                # return image name back to calling method to use it for thumbnail downloads
                download_status = 'success'
                download_message = "Completed Image ====> " + prefix + str(count) + "_ " + image_name
                return_image_name = prefix + str(count) + "_ " + image_name  # _ instead of . to preserve extensions.

                # image size parameter
                if print_size:
                    logging.info("Image Size: %s" % str(GoogleImageDownload.file_size(path)))

            except UnicodeEncodeError as error:
                download_status = 'fail'
                download_message = "UnicodeEncodeError on an image...trying next one..." + " Error: " + str(error)
                return_image_name = ''
                absolute_path = ''

            except URLError as error:
                download_status = 'fail'
                download_message = "URLError on an image...trying next one..." + " Error: " + str(error)
                return_image_name = ''
                absolute_path = ''

        except HTTPError as error:  # If there is any HTTPError
            download_status = 'fail'
            download_message = "HTTPError on an image...trying next one..." + " Error: " + str(error)
            return_image_name = ''
            absolute_path = ''

        except URLError as error:
            download_status = 'fail'
            download_message = "URLError on an image...trying next one..." + " Error: " + str(error)
            return_image_name = ''
            absolute_path = ''

        except ssl.CertificateError as error:
            download_status = 'fail'
            download_message = "CertificateError on an image...trying next one..." + " Error: " + str(error)
            return_image_name = ''
            absolute_path = ''

        except IOError as error:  # If there is any IOError
            download_status = 'fail'
            download_message = "IOError on an image...trying next one..." + " Error: " + str(error)
            return_image_name = ''
            absolute_path = ''

        except http.client.IncompleteRead as error:
            download_status = 'fail'
            download_message = "IncompleteReadError on an image...trying next one..." + " Error: " + str(error)
            return_image_name = ''
            absolute_path = ''

        return download_status, download_message, return_image_name, absolute_path

    @staticmethod
    def _get_next_item(source):
        """
        Parse the source of the page for the next image.
           :parameter source: Source.
           :return: A tuple made of the final object and the end object;
        """
        start_line = source.find('rg_meta notranslate')
        if start_line == -1:  # If no links are found then give an error!
            end_quote = 0
            link = "no_links"
            return link, end_quote
        else:
            start_line = source.find('class="rg_meta notranslate">')
            start_object = source.find('{', start_line + 1)
            end_object = source.find('</div>', start_object + 1)
            object_raw = str(source[start_object:end_object])
            try:
                object_decode = bytes(object_raw, "utf-8").decode("unicode_escape")
                final_object = json.loads(object_decode)
            except Exception:
                final_object = ""
            return final_object, end_object

    def _get_all_items(self, page, main_directory, dir_name, limit):
        """
        Getting all links with the help of '_images_get_next_image'.
           :parameter page: Page to parse.
           :parameter main_directory: Main directory of the images.
           :parameter dir_name: Directory of the image in the main directory.
           :parameter limit: Limit number of images to download.
           :return: A tuple made of the images, the absolute path of the images and the number of errors.
        """
        items = []
        abs_path = []
        error_count = 0
        i = 0
        count = 1
        while count < limit + 1:
            item, end_content = GoogleImageDownload._get_next_item(page)
            if item == "no_links":
                break
            elif item == "":
                page = page[end_content:]
            elif self.configuration['offset'] and count < int(self.configuration['offset']):
                count += 1
                page = page[end_content:]
            else:
                # format the item for readability
                item = GoogleImageDownload.format_object(item)
                if self.configuration['metadata']:
                    logging.info("Image Metadata: %s" % str(item))

                # download the images
                download_status, download_message, return_image_name, absolute_path = GoogleImageDownload.download_image(
                    item['image_link'], item['image_format'], main_directory, dir_name, count,
                    self.configuration['print_urls'], self.configuration['socket_timeout'],
                    self.configuration['prefix'], self.configuration['print_size'],
                    self.configuration['no_numbering'], self.configuration['no_download'])
                logging.info(download_message)
                if download_status == "success":

                    # download image_thumbnails
                    if self.configuration['thumbnail']:
                        download_status, download_message_thumbnail = GoogleImageDownload.download_image_thumbnail(
                            item['image_thumbnail_url'], main_directory, dir_name, return_image_name,
                            self.configuration['print_urls'], self.configuration['socket_timeout'],
                            self.configuration['print_size'],
                            self.configuration['no_download'])
                        logging.info(download_message_thumbnail)

                    count += 1
                    item['image_filename'] = return_image_name
                    items.append(item)  # Append all the links in the list named 'Links'
                    abs_path.append(absolute_path)
                else:
                    error_count += 1

                # delay param
                if self.configuration['delay']:
                    sleep(int(self.configuration['delay']))

                page = page[end_content:]
            i += 1
        if count < limit:
            logging.warning("All %d were not downloaded. Only %d we got for this search filter!" % (limit, count - 1))
        return items, error_count, abs_path

    def download(self):
        """
        Bulk download method.
           :return: A tuple made of the path of the image and the URL list of the images.
        """
        # for input coming from other python files
        if __name__ != "__main__":
            for arg in ARGS_LIST:
                if arg not in self.configuration:
                    self.configuration[arg] = None

        # Initialization and Validation of user self.configuration
        if self.configuration['keywords']:
            search_keyword = [str(item) for item in self.configuration['keywords'].split(',')]

        if self.configuration['keywords_from_file']:
            search_keyword = GoogleImageDownload.keywords_from_file(self.configuration['keywords_from_file'])

        # both time and time range should not be allowed in the same query
        if self.configuration['time'] and self.configuration['time_range']:
            raise GoogleImageDownloadException(
                'Either time or time range should be used in a query. Both cannot be used at the same time.')

        # both time and time range should not be allowed in the same query
        if self.configuration['size'] and self.configuration['exact_size']:
            raise ValueError(
                'Either "size" or "exact_size" should be used in a query. Both cannot be used at the same time.')

        # both image directory and no image directory should not be allowed in the same query
        if self.configuration['image_directory'] and self.configuration['no_directory']:
            raise ValueError('You can either specify image directory or specify no image directory, not both!')

        # Additional words added to keywords
        if self.configuration['suffix_keywords']:
            suffix_keywords = [" " + str(sk) for sk in self.configuration['suffix_keywords'].split(',')]
        else:
            suffix_keywords = ['']

        # Additional words added to keywords
        if self.configuration['prefix_keywords']:
            prefix_keywords = [str(sk) + " " for sk in self.configuration['prefix_keywords'].split(',')]
        else:
            prefix_keywords = ['']

        # Setting limit on number of images to be downloaded
        if self.configuration['limit']:
            limit = int(self.configuration['limit'])
        else:
            limit = 100

        if self.configuration['url']:
            current_time = str(datetime.datetime.now()).split('.')[0]
            search_keyword = [current_time.replace(":", "_")]

        if self.configuration['similar_images']:
            current_time = str(datetime.datetime.now()).split('.')[0]
            search_keyword = [current_time.replace(":", "_")]

        # If single_image or url argument not present then keywords is mandatory argument
        if self.configuration['single_image'] is None and self.configuration['url'] is None \
                and self.configuration['similar_images'] is None and \
                self.configuration['keywords'] is None and self.configuration['keywords_from_file'] is None:
            logging.warning(
                "Uh oh! Keywords is a required argument. Please refer to the documentation on guide to writing queries")
            sys.exit()

        # If this argument is present, set the custom output directory
        if self.configuration['output_directory']:
            main_directory = self.configuration['output_directory']
        else:
            main_directory = "downloads"

        # Proxy settings
        if self.configuration['proxy']:
            os.environ["http_proxy"] = self.configuration['proxy']
            os.environ["https_proxy"] = self.configuration['proxy']
            # Initialization Complete

        paths = {}
        for pky in prefix_keywords:
            for sky in suffix_keywords:  # 1.for every suffix keywords
                i = 0
                while i < len(search_keyword):  # 2.for every main keyword
                    iteration = "Item no.: " + str(i + 1) + " -->" + " Item name = " + str(pky) + str(
                        search_keyword[i] + str(sky))
                    logging.info(iteration)
                    logging.info("Evaluating...")
                    search_term = pky + search_keyword[i] + sky

                    if self.configuration['image_directory']:
                        dir_name = self.configuration['image_directory']
                    elif self.configuration['no_directory']:
                        dir_name = ''
                    else:
                        dir_name = search_term + (
                            '-' + self.configuration['color'] if self.configuration['color'] else '')  # sub-directory

                    GoogleImageDownload.create_directories(main_directory, dir_name,
                                                           self.configuration['thumbnail'])  # create directories in OS

                    params = self.build_url_parameters()  # building URL with params

                    url = self.build_search_url(search_term, params, self.configuration['url'],
                                                self.configuration['similar_images'],
                                                self.configuration['specific_site'],
                                                self.configuration['safe_search'])  # building main search url

                    if limit < 101:
                        raw_html = GoogleImageDownload.download_page(url)  # download page
                    else:
                        raw_html = GoogleImageDownload.download_extended_page(url,
                                                                              self.configuration['chrome_driver_path'])

                    if self.configuration['no_download']:
                        logging.info("Starting to Print Image URLS")
                    else:
                        logging.info("Starting Download...")
                    # get all image items and download images
                    items, error_count, abs_path = self._get_all_items(raw_html, main_directory, dir_name, limit)
                    paths[pky + search_keyword[i] + sky] = abs_path

                    # dumps into a json file
                    if self.configuration['extract_metadata']:
                        try:
                            if not os.path.exists("logs"):
                                os.makedirs("logs")
                        except OSError as error:
                            logging.warning(error)
                        json_file = open("logs/" + search_keyword[i] + ".json", "w")
                        json.dump(items, json_file, indent=4, sort_keys=True)
                        json_file.close()

                    # Related images
                    if self.configuration['related_images']:
                        logging.info("Getting list of related keywords...this may take a few moments")
                        tabs = GoogleImageDownload.get_all_tabs(raw_html)
                        for key, value in tabs.items():
                            final_search_term = (search_term + " - " + key)
                            logging.info("Now Downloading - %s" % final_search_term)
                            if limit < 101:
                                new_raw_html = GoogleImageDownload.download_page(value)  # download page
                            else:
                                new_raw_html = GoogleImageDownload.download_extended_page(value,
                                                                                          self.configuration[
                                                                                              'chrome_driver_path'])
                            GoogleImageDownload.create_directories(main_directory, final_search_term,
                                                                   self.configuration['thumbnail'])
                            self._get_all_items(new_raw_html, main_directory, search_term + " - " + key, limit)

                    i += 1
                    logging.warning("Errors: %d" % error_count)
        if self.configuration['print_paths']:
            logging.info(paths)
        return paths, url


# ------------- Main Program -------------#
def main():
    """
    Main function executed when the script in run command line.:
    """
    records = user_input()
    for arguments in records:

        if arguments['single_image']:  # Download Single Image using a URL
            GoogleImageDownload.single_image(arguments['single_image'])
        else:  # or download multiple images based on keywords/keyphrase search
            time_0 = perf_counter()  # start the timer
            response = GoogleImageDownload(arguments)
            response.download()

            logging.info("Everything downloaded!")
            time_1 = perf_counter()  # stop the timer
            #  Calculating the total time required to crawl, find and download all the links of 60,000 images
            total_time = time_1 - time_0
            logging.info("Total time taken: %11.2f seconds."% total_time)


if __name__ == "__main__":
    """
    Entry point of the script when executed in command line.
    """
    main()
