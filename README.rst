Google Images Download
######################

Python Script for 'searching' and 'downloading' giant image datasets from Google images to the local hard disk!
It's more of less the fork number 800 of the `googleimages-download library <https://github.com/hardikvasa/google-images-download/>`__.
With more than 4 thousand stars on GitHub the library surely filled 100% dataset creator needs. On the other hand, it
seemed hard to maintain for various reasons. One of them being the ython2/3 compatibility leading to many
if/else when using urllib. This one being completely different between Python 2 and 3. This fork only support Python 3.
The original library did not comply Pythonic standards in term of coding, readability, testing and documentation. It
therefore create a technical debt.

.. contents:: :local:

Summary
=======

This is a command line Python program to search keywords/key-phrases on Google Images
and optionally download images to your computer. You can also invoke this script from
another Python file.

This is a small and ready-to-run program. No dependencies are required to be installed
if you would only want to download up to 100 images per keyword. If you would want **more than 100
images** per keyword, then you would need to install ``Selenium`` library along with ``chromedriver``.
Detailed instructions in the troubleshooting section.

Library structure
=================

.. code-block:: bash

    .
    ├── build.sh
    ├── docs
    │   └── source
    │       ├── conf.py
    │       ├── index.rst
    │       └── papit.png
    ├── google_images_download
    │   ├── google_images_download.py
    │   ├── __init__.py
    │   ├── __main__.py
    │   └── sample_config.json
    ├── tests
    │   ├── __init__.py
    │   ├── test_google_images_download.py
    │   └── test_sample.py
    ├── install.sh
    ├── make.bat
    ├── Makefile
    ├── MANIFEST.in
    ├── README.rst
    ├── requirements.txt
    ├── review-test.sh
    ├── setup.cfg
    ├── setup.py
    ├── tests

Build
=====

.. code-block:: bash

    $ git clone https://github.com/phe-sto/google-images-download.git
    $ python3 setup.py bdist_wheel
    OR
    $ python setup.py bdist_wheel
    OR
    sh build.sh

The ``build.sh`` also build the sphinx documentation in HTML format.

Installation
============

.. code-block:: bash

    $ git clone https://github.com/phe-sto/google-images-download.git
    $ cd google-images-download && sudo Python3 setup.py install
    OR
    $ python3 -m pip install google_images_download-0.1-py2.py3-none-any.whl
    OR
    sh install.sh

Manually using UI

Go to the `repo on github <https://github.com/phe-sto/google-images-download>`__ -> Click on 'Clone or Download' -> Click on 'Download ZIP' and save it on your local disk.

Test and review
===============

A basic code review is performed `pylint <https://www.pylint.org>`__. Test from the ``tests`` directory are scheduled
using the amazing testing framework `pytest <https://docs.pytest.org>`__. `Coverage <https://coverage.readthedocs.io>`__
is also used to produce a coverage report. `Tox <https://tox.readthedocs.io>`__ is also used to test the package.

.. code-block:: bash

    sh review-test.sh

**Test report**

Consult the current `test report <https://www.papit.fr/google-images-download/test>`__.

**Coverage report**

Consult the current `test coverage report report <https://www.papit.fr/google-images-download/coverage>`__.

Contribute
==========

Anyone is welcomed and even encouraged to contribute to this project.
If you would like to make a change, open a pull request. Please do not forget to update tests and run the
``review-test.sh`` script that produce test and coverage reports. All new Python shall be documented using docstrings in
reStructuredText to be included in `sphinx documentation framework <https://Pythonhosted.org/an_example_pypi_project/sphinx.html>`__.
For issues and discussion visit the `Issue Tracker <https://github.com/phe-sto/google-images-download/issues>`__.
The aim of this repo is to keep it simple, stand-alone and compliant with Python development standards.

Full API documentation
======================

The full documentation can be founded under the developer `PapIT website <https://www.papit.fr/google-images-download>`__.

Compatibility
=============

This program is compatible with Python 3.x only.
It is a download-and-run program with no changes to the file.
You will just have to specify parameters through the command line.

Usage - Using Command Line Interface
====================================

If installed via pip or using CLI, use the following command:

.. code-block:: bash

    $ google-image-download[Arguments...]

If downloaded via the UI, unzip the file downloaded, go to the 'google_images_download' directory and use one of the below commands:

.. code-block:: bash

    $ python3 google_images_download.py [Arguments...]
    OR
    $ python google_images_download.py [Arguments...]


Usage - From another Python script
==================================

If you would want to use this library from another Python file, you could use it as shown below:

.. code-block:: python

    from google_images_download import google_images_download

    response = google_images_download.GoogleImageDownload({<Arguments...>})
    absolute_image_paths, url = response.download()


Arguments
=========

+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| Argument          | Short hand  | Description                                                                                                                   |
+===================+=============+===============================================================================================================================+
| config_file       | cf          | You can pass the arguments inside a config file. This is an alternative to passing arguments on the command line directly.    |
|                   |             |                                                                                                                               |
|                   |             | Please refer to the                                                                                                           |
|                   |             | `config file format <https://github.com/phe-sto/google-images-download/blob/master/README.rst#config-file-format>`__ below    |
|                   |             |                                                                                                                               |
|                   |             | * If 'config_file' argument is present, the program will use the config file and command line arguments will be discarded     |
|                   |             | * Config file can only be in **JSON** format                                                                                  |
|                   |             | * Please refrain from passing invalid arguments from config file. Refer to the below arguments list                           |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| keywords          | k           | Denotes the keywords/key phrases you want to search for. For more than one keywords, wrap it in single quotes.                |
|                   |             |                                                                                                                               |
|                   |             | Tips:                                                                                                                         |
|                   |             |                                                                                                                               |
|                   |             | * If you simply type the keyword, Google will best try to match it                                                            |
|                   |             | * If you want to search for exact phrase, you can wrap the keywords in double quotes ("")                                     |
|                   |             | * If you want to search to contain either of the words provided, use **OR** between the words.                                |
|                   |             | * If you want to explicitly not want a specific word use a minus sign before the word (-)                                     |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| keywords_from_file| kf          | Denotes the file name from where you would want to import the keywords.                                                       |
|                   |             |                                                                                                                               |
|                   |             | Add one keyword per line. Blank/Empty lines are truncated automatically.                                                      |
|                   |             |                                                                                                                               |
|                   |             | Only file types '.txt' or  '.csv' are allowed.                                                                                |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| prefix_keywords   | pk          | Denotes additional words added before main keyword while making the search query.                                             |
|                   |             |                                                                                                                               |
|                   |             | The final search query would be: <prefix keyword> <keyword>                                                                   |
|                   |             |                                                                                                                               |
|                   |             | So, for example, if the keyword is 'car' and prefix_keyword is 'red,yellow,blue', it will search and download images for      |
|                   |             | 'red car', 'yellow car' and 'blue car' individually                                                                           |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| suffix_keywords   | sk          | Denotes additional words added after main keyword while making the search query.                                              |
|                   |             |                                                                                                                               |
|                   |             | The final search query would be: <keyword> <suffix keyword>                                                                   |
|                   |             |                                                                                                                               |
|                   |             | So, for example, if the keyword is 'car' and suffix_keyword is 'red,yellow,blue', it will search and download images for      |
|                   |             | 'car red', 'car yellow' and 'car blue' individually                                                                           |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| limit             | l           | Denotes number of images that you want to download.                                                                           |
|                   |             |                                                                                                                               |
|                   |             | You can specify any integer value here. It will try and get all the images that it finds in the google image search page.     |
|                   |             |                                                                                                                               |
|                   |             | If this value is not specified, it defaults to 100.                                                                           |
|                   |             |                                                                                                                               |
|                   |             | **Note**: In case of occasional errors while downloading images, you could get less than 100 (if the limit is set to 100)     |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| related_images    | ri          | This argument downloads a ton of images related to the keyword you provided.                                                  |
|                   |             |                                                                                                                               |
|                   |             | Google Images page returns list of related keywords to the keyword you have mentioned in the query. This tool downloads       |
|                   |             | images from each of those related keywords based on the limit you have mentioned in your query                                |
|                   |             |                                                                                                                               |
|                   |             | This argument does not take any value. Just add '--related_images' or '-ri' in your query.                                    |
|                   |             |                                                                                                                               |
|                   |             | **Note:**  This argument can download hundreds or thousands of additional images so please use this carefully.                |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| format            | f           | Denotes the format/extension of the image that you want to download.                                                          |
|                   |             |                                                                                                                               |
|                   |             | `Possible values: jpg, gif, png, bmp, svg, webp, ico`                                                                         |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| color             | co          | Denotes the color filter that you want to apply to the images.                                                                |
|                   |             |                                                                                                                               |
|                   |             | `Possible values: red, orange, yellow, green, teal, blue, purple, pink, white, gray, black, brown`                            |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| color_type        | ct          | Denotes the color type you want to apply to the images.                                                                       |
|                   |             |                                                                                                                               |
|                   |             | `Possible values: full-color, black-and-white, transparent`                                                                   |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| usage_rights      | r           | Denotes the usage rights/licence under which the image is classified.                                                         |
|                   |             |                                                                                                                               |
|                   |             | `Possible values:`                                                                                                            |
|                   |             |                                                                                                                               |
|                   |             | * `labeled-for-reuse-with-modifications`,                                                                                     |
|                   |             | * `labeled-for-reuse`,                                                                                                        |
|                   |             | * `labeled-for-noncommercial-reuse-with-modification`,                                                                        |
|                   |             | * `labeled-for-nocommercial-reuse`                                                                                            |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| size              | s           | Denotes the relative size of the image to be downloaded.                                                                      |
|                   |             |                                                                                                                               |
|                   |             | `Possible values: large, medium, icon, >400*300, >640*480, >800*600, >1024*768, >2MP, >4MP, >6MP, >8MP, >10MP,                |
|                   |             | >12MP, >15MP, >20MP, >40MP, >70MP`                                                                                            |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| exact_size        | es          | You can specify the exact size/resolution of the images                                                                       |
|                   |             |                                                                                                                               |
|                   |             | This value of this argument can be specified as ``<integer,integer>`` where the fist integer stands for width of the image    |
|                   |             | and the second integer stands for the height of the image. For example, ``-es 1024,786``                                      |
|                   |             |                                                                                                                               |
|                   |             | **Note**: You cannot specify both 'size' and 'exact_size' arguments in the same query. You can only give one of them.         |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| aspect_ratio      | a           | Denotes the aspect ratio of images to download.                                                                               |
|                   |             |                                                                                                                               |
|                   |             | `Possible values: tall, square, wide, panoramic`                                                                              |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| type              | t           | Denotes the type of image to be downloaded.                                                                                   |
|                   |             |                                                                                                                               |
|                   |             | `Possible values: face, photo, clipart, line-drawing, animated`                                                               |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| time              | w           | Denotes the time the image was uploaded/indexed.                                                                              |
|                   |             |                                                                                                                               |
|                   |             | `Possible values: past-24-hours, past-7-days`                                                                                 |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| time_range        | wr          | Denotes the time range for which you want to search the images                                                                |
|                   |             |                                                                                                                               |
|                   |             | The value of this parameter should be in the following format {"time_min":"MM/DD/YYYY","time_max":"MM/DD/YYYY"}               |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| delay             | d           | Time to wait between downloading two images                                                                                   |
|                   |             |                                                                                                                               |
|                   |             | Time is to be specified in seconds. But you can have sub-second times by using decimal points.                                |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| url               | u           | Allows you search by image when you have the URL from the Google Images page.                                                 |
|                   |             | It downloads images from the google images link provided                                                                      |
|                   |             |                                                                                                                               |
|                   |             | If you are searching an image on the browser google images page, simply grab the browser URL and paste it in this parameter   |
|                   |             | It will download all the images seen on that page.                                                                            |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| single_image      | x           | Allows you to download one image if the complete (absolute) URL of the image is provided                                      |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| output_directory  | o           | Allows you specify the main directory name in which the images are downloaded.                                                |
|                   |             |                                                                                                                               |
|                   |             | If not specified, it will default to 'downloads' directory. This directory is located in the path from where you run this code|
|                   |             |                                                                                                                               |
|                   |             | The directory structure would look like: ``<output_directory><image_directory><images>``                                      |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| image_directory   | i           | This lets you specify a directory inside of the main directory (output_directory) in which the images will be saved           |
|                   |             |                                                                                                                               |
|                   |             | If not specified, it will default to the name of the keyword.                                                                 |
|                   |             |                                                                                                                               |
|                   |             | The directory structure would look like: ``<output_directory><image_directory><images>``                                      |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| no_directory      | n           | This option allows you download images directly in the main directory (output_directory) without an image_directory           |
|                   |             |                                                                                                                               |
|                   |             | The directory structure would look like: ``<output_directory><images>``                                                       |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| proxy             | px          | Allows you to specify proxy server setting for all your requests                                                              |
|                   |             |                                                                                                                               |
|                   |             | You can specify the proxy settings in 'IP:Port' format                                                                        |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| similar_images    | si          | Reverse Image Search or 'Search by Image' as it is referred to on Google.                                                     |
|                   |             |                                                                                                                               |
|                   |             | Searches and downloads images that are similar to the absolute image link/url you provide.                                    |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| specific_site     | ss          | Allows you to download images with keywords only from a specific website/domain name you mention.                             |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| print_urls        | p           | Print the URLs of the images on the console. These image URLs can be used for debugging purposes                              |
|                   |             |                                                                                                                               |
|                   |             | This argument does not take any value. Just add '--print_urls' or '-p' in your query.                                         |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| print_size        | ps          | Prints the size of the images on the console                                                                                  |
|                   |             |                                                                                                                               |
|                   |             | The size denoted the actual size of the image and not the size of the image on disk                                           |
|                   |             |                                                                                                                               |
|                   |             | This argument does not take any value. Just add '--print_size' or '-ps' in your query.                                        |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| print_paths       | pp          | Prints the list of all the absolute paths of the downloaded images                                                            |
|                   |             |                                                                                                                               |
|                   |             | When calling the script from another Python file, this list will be saved in a variable (as shown in the example below)       |
|                   |             |                                                                                                                               |
|                   |             | This argument also allows you to print the list on the console                                                                |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| metadata          | m           | Prints the metada of the image on the console.                                                                                |
|                   |             |                                                                                                                               |
|                   |             | This includes image size, origin, image attributes, description, image URL, etc.                                              |
|                   |             |                                                                                                                               |
|                   |             | This argument does not take any value. Just add '--metadata' or '-m' in your query.                                           |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| extract_metadata  | e           | This option allows you to save metadata of all the downloaded images in a JSON file.                                          |
|                   |             |                                                                                                                               |
|                   |             | This file can be found in the ``logs/`` directory. The name of the file would be same as the keyword nam                      |
|                   |             |                                                                                                                               |
|                   |             | This argument does not take any value. Just add '--extract_metadata' or '-e' in your query.                                   |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| socket_timeout    | st          | Allows you to specify the time to wait for socket connection.                                                                 |
|                   |             |                                                                                                                               |
|                   |             | You could specify a higher timeout time for slow internet connection. The default value is 10 seconds.                        |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| thumbnail         | th          | Downloads image thumbnails corresponding to each image downloaded.                                                            |
|                   |             |                                                                                                                               |
|                   |             | Thumbnails are saved in their own sub-directories inside of the main directory.                                               |
|                   |             |                                                                                                                               |
|                   |             | This argument does not take any value. Just add '--thumbnail' or '-th' in your query.                                         |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| language          | la          | Defines the language filter. The search results are automatically returned in that language                                   |
|                   |             |                                                                                                                               |
|                   |             | `Possible Values: Arabic, Chinese (Simplified), Chinese (Traditional), Czech, Danish, Dutch, English, Estonian. Finnish,      |
|                   |             | French, German, Greek, Hebrew, Hungarian, Icelandic, Italian, Japanese, Korean, Latvianm, Lithuanian, Norwegian, Portuguese,  |
|                   |             | Polish, Romanian, Russian, Spanish, Swedish, Turkish`                                                                         |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| prefix            | pr          | A word that you would want to prefix in front of actual image name.                                                           |
|                   |             |                                                                                                                               |
|                   |             | This feature can be used to rename files for image identification purpose.                                                    |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| chromedriver      | cd          | With this argument you can pass the path to the 'chromedriver'.                                                               |
|                   |             |                                                                                                                               |
|                   |             | The path looks like this: "path/to/chromedriver". In windows it will be "C:\\path\\to\\chromedriver.exe"                      |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| safe_search       | sa          | Searches for images with the Safe Search filter On                                                                            |
|                   |             |                                                                                                                               |
|                   |             | And this filter will be Off by default if you do not specify the safe_search argument                                         |
|                   |             |                                                                                                                               |
|                   |             | This argument does not take any value. Just add '--safe_search' or '-sa' in your query.                                       |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| no_numbering      | nn          | When you specify this argument, the script does not add ordered numbering as prefix to the images it downloads                |
|                   |             |                                                                                                                               |
|                   |             | If this argument is not specified, the images are numbered in order in which they are downloaded                              |
|                   |             |                                                                                                                               |
|                   |             | This argument does not take any value. Just add '--no_numbering' or '-nn' in your query.                                      |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| offset            | of          | When you specify this argument, it will skip the offset number of links before it starts downloading images                   |
|                   |             |                                                                                                                               |
|                   |             | If this argument is not specified, the script will start downloading form the first link until the limit is reached           |
|                   |             |                                                                                                                               |
|                   |             | This argument takes integer. Make sure the value of this argument is less than the value of limit                             |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| no_download       | nd          | Print the URLs of the images on the console without downloading them. These image URLs can be used for debugging purposes     |
|                   |             |                                                                                                                               |
|                   |             | This argument does not take any value. Just add '--no-download' or '-nd' in your query.                                       |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| help              | h           | show the help message regarding the usage of the above arguments                                                              |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+


**Note:** If ``single_image`` or ``url`` parameter is not present, then keywords is a mandatory parameter. No other parameters are mandatory.

Config File Format
==================

You can either pass the arguments directly from the command as in the examples below or you can pass it through a config file. Below is a sample of how a config
file looks.

You can pass more than one record through a config file. The below sample consist of two set of records. The code will iterate through each of the record and
download images based on arguments passed.

.. code:: json

    {
        "Records": [
            {
                "keywords": "apple",
                "limit": 5,
                "color": "green",
                "print_urls": true
            },
            {
                "keywords": "universe",
                "limit": 15,
                "size": "large",
                "print_urls": true
            }
        ]
    }


Examples
========

- If you are calling this library from another Python file, below is the sample code

.. code-block:: python

    from google_images_download import google_images_download   #importing the library

    response = google_images_download.GoogleImageDownload()   #class instantiation

    arguments = {"keywords": "Polar bears,baloons,Beaches", "limit": 20, "print_urls": True}   # creating list of arguments
    paths = response.download(arguments)   #passing the arguments to the function
    print(paths)   #printing absolute paths of the downloaded images

- If you are passing arguments from a config file, simply pass the config_file argument with name of your JSON file

.. code-block:: bash

    $ google-image-download-cf example.json

- Simple example of using keywords and limit arguments

.. code-block:: bash

    $ google-image-download--keywords "Polar bears, baloons, Beaches" --limit 20

-  Using Suffix Keywords allows you to specify words after the main
   keywords. For example if the ``keyword = car`` and
   ``suffix keyword = 'red,blue'`` then it will first search for
   ``car red`` and then ``car blue``

.. code-block:: bash

    $ google-image-download--k "car" -sk 'red,blue,white' -l 10

-  To use the short hand command

.. code-block:: bash

    $ google-image-download-k "Polar bears, baloons, Beaches" -l 20

-  To download images with specific image extension/format

.. code-block:: bash

    $ google-image-download--keywords "logo" --format svg

-  To use color filters for the images

.. code-block:: bash

    $ google-image-download-k "playground" -l 20 -co red

-  To use non-English keywords for image search

.. code-block:: bash
    
    $ google-image-download-k "北极熊" -l 5

-  To download images from the google images link

.. code-block:: bash
    
    $ google-image-download-k "sample" -u <google images page URL>

-  To save images in specific main directory (instead of in 'downloads')

.. code-block:: bash
    
    $ google-image-download-k "boat" -o "boat_new"

-  To download one single image with the image URL

.. code-block:: bash
    
    $ google-image-download--keywords "baloons" --single_image <URL of the images>

-  To download images with size and type constrains

.. code-block:: bash
    
    $ google-image-download--keywords "baloons" --size medium --type animated

-  To download images with specific usage rights

.. code-block:: bash
    
    $ google-image-download--keywords "universe" --usage_rights labeled-for-reuse

-  To download images with specific color type

.. code-block:: bash
    
    $ google-image-download--keywords "flowers" --color_type black-and-white

-  To download images with specific aspect ratio

.. code-block:: bash
    
    $ google-image-download--keywords "universe" --aspect_ratio panoramic

-  To download images which are similar to the image in the image URL that you provided (Reverse Image search).

.. code-block:: bash
    
    $ google-image-download-si <image url> -l 10

-  To download images from specific website or domain name for a given keyword

.. code-block:: bash
    
    $ google-image-download--keywords "universe" --specific_site example.com

The images would be downloaded in their own sub-directories inside the main directory
(either the one you provided or in 'downloads') in the same folder you are in.


Flow Chart
==========

``QUERY FORMATING`` > ``DOWNLOAD HTML`` > ``SCRAP LINKS`` > ``SAVE IMAGES``

--------------

Troubleshooting Errors/Issues
=============================

**SSL Errors**

.. warning::
    If you do see SSL errors on Mac for Python 3,
    please go to Finder —> Applications —> Python 3 —> Click on the ‘Install Certificates.command’
    and run the file.

**GoogleImageDownload: command not found**

.. warning::
    While using the above commands, if you get ``Error: -bash: GoogleImageDownload: command not found`` then you have to set the correct path variable.
    To get the details of the repo, run the following command:

.. code-block:: bash

    $ pip show -f google_images_download
    OR
    $ pip3 show -f google_images_download

you will get the result like this:

.. code-block:: bash

    Name: google-images-download
    Version: 0.1
    Summary: Python Script to download giant dataset of images from 'Google Images'. It is a ready-to-run code!
    Home-page: https://github.com/phe-sto/google-images-download
    Author: Christohe Brun
    Author-email: christophe.brun@papit.fr
    License: NO LICENSE, FEEL FREE!
    Location: /home/chrichri/.local/lib/python3.6/site-packages
    Requires: pytest, pytest-html, coverage, sphinx, sphinx-bootstrap-theme, pylint, tox, selenium
    Files:
      ../../../bin/google-images-download
      google_images_download-0.1.dist-info/DESCRIPTION.rst
      google_images_download-0.1.dist-info/INSTALLER
      google_images_download-0.1.dist-info/METADATA
      google_images_download-0.1.dist-info/RECORD
      google_images_download-0.1.dist-info/WHEEL
      google_images_download-0.1.dist-info/entry_points.txt
      google_images_download-0.1.dist-info/metadata.json
      google_images_download-0.1.dist-info/top_level.txt
      google_images_download/__init__.py
      google_images_download/__main__.py
      google_images_download/__pycache__/__init__.cpython-36.pyc
      google_images_download/__pycache__/__main__.cpython-36.pyc
      google_images_download/__pycache__/google_images_download.cpython-36.pyc
      google_images_download/google_images_download.py

**Permission denied creating directory 'downloads'**

When you run the command, it downloads the images in the current directory (the directory from where you are running the command). If you get permission denied error for creating the `downloads directory`, then move to a directory in which you have the write permission and then run the command again.


**Permission denied while installing the library**

On MAC and Linux, when you get permission denied when installing the library using pip, try doing a user install.

.. code-block:: bash
	
    $ python3 -m pip install google_images_download-0.1-py2.py3-none-any.whl --user

You can also run pip install as a superuser with ``sudo pip3 install google_images_download-0.1-py2.py3-none-any.whl``
but it is not generally a good idea because it can cause issues with your system-level packages.


**Installing the chromedriver (with Selenium)**

If you would want to download more than 100 images per keyword, then you will need to install 'selenium' library along with 'chromedriver' extension.

If you have pip-installed the library or had run the setup.py file, Selenium would have automatically installed on your machine. You will also need Chrome browser on your machine. For chromedriver:

`Download the correct chromedriver <https://sites.google.com/a/chromium.org/chromedriver/downloads>`__ based on your operating system.

On **Windows** or **MAC** if for some reason the chromedriver gives you trouble, download it under the current directory and run the command.

On windows however, the path to chromedriver has to be given in the following format:

``C:\\complete\\path\\to\\chromedriver.exe``

On **Linux** if you are having issues installing google chrome browser, refer to this `CentOS or Amazon Linux Guide <https://intoli.com/blog/installing-google-chrome-on-centos/>`__
or `Ubuntu Guide <https://askubuntu.com/questions/510056/how-to-install-google-chrome in documentation>`__

For **All the operating systems** you will have to use '--chromedriver' or '-cd' argument to specify the path of
chromedriver that you have downloaded in your machine.

If on any rare occasion the chromedriver does not work for you, try downgrading it to a lower version.

Donation
========

You can donate to support Python and Open Source development.

**BTC** ``32JSkGXcBK2dirP6U4vCx9YHHjV5iSYb1G``

**ETH** ``0xF556505d13aC9a820116d43c29dc61417d3aB2F8``

Disclaimer
==========

This program lets you download tons of images from Google.
Please do not download or use any image that violates its copyright terms.
Google Images is a search engine that merely indexes images and allows you to find them.
It does NOT produce its own images and, as such, it doesn't own copyright on any of them.
The original creators of the images own the copyrights.

Images published in the United States are automatically copyrighted by their owners,
even if they do not explicitly carry a copyright warning.
You may not reproduce copyright images without their owner's permission,
except in "fair use" cases,
or you could risk running into lawyer's warnings, cease-and-desist letters, and copyright suits.
Please be very careful before its usage!
